import datetime
import json as simplejson

from django.http import JsonResponse
from django.contrib.auth import hashers
from django import db
from stuff import models #TODO: import specific models from .models, to prevent having to retype models everytime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers



#Tested
def create_user(request):
    if request.method != 'POST':
        #return HttpResponse("must make POST", status=400)
        return _error_response(request, "must make POST request")
    if 'usertype' not in request.POST:
        return _error_response(request, "Usertype is not found")

    if 'password' not in request.POST or 'username' not in request.POST:
        return _error_response(request, "missing fields for Basic User")
    if request.POST['usertype'] == 'buyer' and 'resume_url' not in request.POST:
        return _error_response(request, "missing fields for Buyer")
    if request.POST['usertype'] == 'seller' and 'company_name' not in request.POST:
        return _error_response(request, "missing fields for Seller")

    ##create_user
    u = models.User(username=request.POST['username'],
                    password=hashers.make_password(request.POST['password']),
                    usertype=request.POST['usertype'])
    try:
        u.save()
    except db.Error:
        return _error_response(request, "can't store User. db error")



    ##create seller
    if(request.POST['usertype'] == 'seller'):
        s = models.Seller(company=models.Company.objects.get(name=request.POST['company_name']), user_account=u)
        try:
             s.save()
        except db.Error:
            return _error_response(request, "can't store Seller. db error")
            #return HttpResponse("can't write into DB",status=500)
        return _success_response(request, {'seller_id': s.pk})




    ##create buyer
    if(request.POST['usertype'] == 'buyer'):
        b = models.Buyer(resume_url=request.POST['resume_url'], user_account=u)
        try:
            b.save()
        except db.Error:
            return _error_response(request, "can't store Seller. db error")
        return _success_response(request, {'buyer_id': b.pk})


def view_all_buyers(request):
    all_buyers = models.Buyer.objects.all()
    return JsonResponse({'ok': True, 'buyer_list': all_buyers})

def view_all_sellers(request):
    all_sellers = models.Seller.objects.all()
    return JsonResponse({'ok': True, 'seller_list': all_sellers})




#Tested
def lookup_user(request, user_id):
    if  request.method !='GET':
        return _error_response(request, "must make GET request")
    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")
    if(u.usertype=='seller'):
        #s = models.Seller.objects.get(user_account=u)
        s = get_object_or_404(models.Seller, user_account=u)
        return _success_response(request, {'username': u.username,
                                            'usertype': u.usertype,
                                            'company': s.company.name})
    if(u.usertype=='buyer'):
        #b = models.Buyer.objects.get(user_account=u)
        b = get_object_or_404(models.Buyer, user_account=u)
        return _success_response(request, {'username': u.username,
                                            'usertype': u.usertype,
                                            'resume':b.resume_url})


def all_sellers(request):
    if request.method!= 'GET':
        return _error_response(request, "must make GET request")

    try:
        seller_list = []
        sellers = models.Seller.objects.all()
        for s in sellers:
            s_info = {'username': s.user_account.username,
                      'id': s.user_account.pk,
                      'company': s.company.name
                      }
            seller_list.append(s_info)
        #data = serializers.serialize('json', seller_list)
    except:
         return _error_response(request, 'could not retrieve sellers.')
    return _success_response(request, simplejson.dumps(seller_list))





def all_buyers(request):
    if request.method!= 'GET':
        return _error_response(request, "must make GET request")
    try:
        #sellers = models.User.objects.filter(usertype='seller')
        buyers = models.Buyer.objects.all()
        data = serializers.serialize('json', buyers)
    except:
         return _error_response(request, 'could not retrieve sellers.')
    return _success_response(request, data)


#Tested
def create_transaction(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'buyer_u_id' not in request.POST or 'seller_u_id' not in request.POST or 'negotiation' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        bua = models.User.objects.get(pk=request.POST['buyer_u_id'])
        buyer = models.Buyer.objects.get(user_account=bua)
    except models.Buyer.DoesNotExist:
        return _error_response(request, "buyer not found")
    try:
        sua = models.User.objects.get(pk=request.POST['seller_u_id'])
        seller = models.Seller.objects.get(user_account=sua)
    except models.Buyer.DoesNotExist:
        return _error_response(request, 'seller not found')
    t = models.Transaction(seller=seller, buyer=buyer, negotiation=request.POST['negotiation'])
    try:
        t.save()
    except db.Error:
        return _error_response(request, "can't store Transaction. db error")
    return _success_response(request, {'transaction_id': t.pk})



def view_all_transactions(request):
    all_transactions = models.Transaction.objects.all()
    return JsonResponse({'ok': True, 'transaction_list': all_transactions})


def create_JobApplication(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'buyer_u_id' not in request.POST or 'company_name' not in request.POST or 'greeting' not in request.POST or 'detail' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        buyer = models.objects.get(pk=request.POST['buyer_id'])
    except models.Buyer.DoesNotExist:
        return _error_response(request, "buyer not found")
    a = models.JobApplication(company=models.Company.get(name=request.POST['company_name']), buyer=buyer, greeting=request.POST['greeting'], detail=request.POST['detail'])
    try:
        a.save()
    except db.Error:
        return _error_response(request, "can't store JobApplication. db error")

def view_company_JobApplications(request, company_id):
    if  request.method !='GET':
        return _error_response(request, "must make GET request")
    try:
        cur_company = get_object_or_404(models.Company, id=company_id)
        job_application_list = models.JobApplication.objects.all().filter(company=cur_company)
    except models.Company.DoesNotExist:
        return _error_response(request, "company not found")

    return _success_response(request, {'job_application_list': job_application_list})



#Tested
def create_company(request):
    if request.method != 'POST':
        return HttpResponse("must make POST", status=400)
    if 'name' not in request.POST or 'description' not in request.POST:
        return _error_response(request, "missing fields")
    #create basic user account
    c = models.Company(name=request.POST['name'], description=request.POST['description'])
    try:
        c.save()
    except db.Error:
        return HttpResponse("DB error", status=500)
    return HttpResponse("Company stored Ok", status=200)





def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})
