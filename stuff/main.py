import datetime
import json

from django.http import JsonResponse
from django.contrib.auth import hashers
from django import db

from stuff import models
from django.http import HttpResponse



def create_user(request):
    if request.method != 'POST':
        #return HttpResponse("must make POST", status=400)
        return _error_response(request, "must make POST request")
    if 'password' not in request.POST or 'username' not in request.POST or 'company_name' not in request.POST or 'usertype' not in request.POST:
        #return HttpResponse("missing required fields",status=400)
        return _error_response(request, "missing fields")
    
    #create basic user account
    u = models.User(username=request.POST['username'],
                    password=hashers.make_password(request.POST['password']),
                    usertype=request.POST['usertype'])
    try:
        u.save()
    except db.Error:
        return _error_response(request, "can't store User. db error")
    #return HttpResponse("DB error",status=400)
    #create seller
    if(request.POST['usertype'] == 'seller'):

        s = models.Seller(company=models.Company.get(name=request.POST['company_name']), user_account=u)
        try:
            s.save()
        except db.Error:
            return _error_response(request, "can't store Seller. db error")
            #return HttpResponse("can't write into DB",status=500)
        return _success_response(request, {'seller_id': s.pk})
        json_data = json.dumps({"selller_id":s.pk})
        return HttpResponse(json_data,status=200 )
    #create buyer
    if(request.POST['usertype'] == 'buyer'):
        b = models.Seller(company=models.Company.get(name=request.POST['company_name']), user_account=u)
        try:
            b.save()
        except db.Error:
            return _error_response(request, "can't store Seller. db error")
        return _success_response(request, {'buyer_id': b.pk})


def lookup_user(reqeust, user_id):
    if reqeust.method !='GET':
        return _error_response(request, "must make GET request")
    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")
    if(u.usertype=='seller'):
        s = models.Seller.objects.get(user_account=u)
        return _success_response(request, {'username': u.username,
                                            'usertype': u.usertype,
                                            'company': s.company})
    if(u.usertype=='buyer'):
        b = models.Buyer.objects.get(user_account=u)
        #b = u.user_set.get()
        return _success_response(request, {'username': u.username,
                                            'usertype': u.usertype,
                                            'resume':b.resume_url})


def create_transaction(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'buyer_id' not in request.POST or 'seller_id' not in request.POST or 'negotiation' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        buyer = models.Buyer.objects.get(pk=request.POST['buyer_id'])
    except models.Buyer.DoesNotExist:
        return _error_response(request, "buyer not found")
    try:
        seller = models.Seller.objects.get(pk=request.POST['seller_id'])
    except models.Buyer.DoesNotExist:
        return _error_response(request, 'seller not found')
    t = models.Transaction(seller=seller, buyer=buyer, negotiation=request.POST['negotiation'])
    try:
        t.save()
    except db.Error:
        return _error_response(request, "can't store Transaction. db error")


def create_JobApplication(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'buyer_id' not in request.POST or 'company_name' not in request.POST or 'greeting' not in request.POST or 'detail' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        buyer = models.Buyer.objects.get(pk=request.POST['buyer_id'])
    except models.Buyer.DoesNotExist:
        return _error_response(request, "buyer not found")
    a = models.JobApplication(company=models.Company.get(name=request.POST['company_name']), buyer=buyer, greeting=request.POST['greeting'], detail=request.POST['detail'])
    try:
        a.save()
    except db.Error:
        return _error_response(request, "can't store JobApplication. db error")


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