import datetime
import json
import os
import base64

from django.http import JsonResponse
from django.contrib.auth import hashers
from django import db
from stuff import models #TODO: import specific models from .models, to prevent having to retype models everytime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta



##Written by Trinity
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

#Tested .. something still require polish
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
        data = {'ok':True,
                'resp': seller_list}
    except:
         return _error_response(request, 'could not retrieve sellers.')
    return HttpResponse(json.dumps(data), content_type='application/json')





#Tested .. something still require polish
def all_buyers(request):
    if request.method!= 'GET':
        return _error_response(request, "must make GET request")
    try:
        buyer_list = []
        buyers = models.Buyer.objects.all()
        for b in buyers:
            b_info = {'username': b.user_account.username,
                      'id': b.user_account.pk,
                      'company': b.resume_url
                      }

            buyer_list.append(b_info)
        #data = serializers.serialize('json', seller_list)
        data = {'ok':True,
                'resp': buyer_list}
    except:
         return _error_response(request, 'could not retrieve sellers.')
    return HttpResponse(json.dumps(data), content_type='application/json')



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



#Tested
def create_JobApplication(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'buyer_u_id' not in request.POST or 'company_name' not in request.POST or 'greeting' not in request.POST or 'detail' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        buyer_user_account = models.User.objects.get(pk=request.POST['buyer_u_id'])
        buyer = models.Buyer.objects.get(user_account=buyer_user_account)
    except models.Buyer.DoesNotExist:
        return _error_response(request, "buyer not found")
    a = models.JobApplication(company=models.Company.objects.get(name=request.POST['company_name']), buyer=buyer, greeting=request.POST['greeting'], detail=request.POST['detail'])
    try:
        a.save()
    except db.Error:
        return _error_response(request, "can't store JobApplication. db error")
    return _success_response(request, {'application_id': a.pk})


#Tested
def create_company(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'name' not in request.POST or 'description' not in request.POST:
        return _error_response(request, "missing fields")
    #create basic user account
    c = models.Company(name=request.POST['name'], description=request.POST['description'])
    try:
        c.save()
    except db.Error:
         return _error_response(request, "DB error, company could not be stored.")
    return _success_response(request, {'company_id': c.pk})


#Tested
def log_in(request):
    if request.method != 'POST':
	    return _error_response(request, "must make POST request")
    if 'username' not in request.POST or 'password' not in request.POST:
        return _error_response(request, "missing fields")
    if models.User.objects.filter(username=request.POST['username']).exists():
        pw = request.POST['password']
        u = models.User.objects.get(username=request.POST['username'])
        if check_password(pw, u.password):
            auth = auth_generetor()
            a = models.Authenticator(user_id = u.pk, authenticator = auth, date_created = datetime.now())
            try:
                a.save()
            except db.Error:
                return _error_response(request, "DB error, authenticator could not be stored.")
            return _success_response(request, {'authenticator': auth})
        else:
            return _error_response(request, "wrong password")
    else:
        return _error_response(request, "username does not exist")
      

def auth_generetor():
    authenticator = base64.b64encode(os.urandom(32)).decode('utf-8')
    return authenticator

#Tested
def log_out(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'user_id' not in request.POST:
        return _error_response(request, "missing user_id")
    delete_auth(request, request.POST['user_id'])
    return _success_response(request, "log out successfully")


#Tested
def check_login(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'authenticator' not in request.POST:
        return _error_response(request, "missing authenticator")
    if models.Authenticator.objects.filter(authenticator=request.POST['authenticator']).exists():
        return _success_response(request, " authenticator is valid")
    


def delete_auth(request, user_id):
    try:
        a = get_object_or_404(models.Authenticator, user_id=user_id).delete()
    except db.Error:
        return _error_response(request, "DB error. can not get auth for the passed user_id.")
    
  
  
##Should I use GET?
##Tested
def check_auth(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'authenticator' not in request.POST:
        return _error_response(request, "missing user_id or authenticator")
    auth_value = request.POST['authenticator']
    if models.Authenticator.objects.filter(authenticator=auth_value).exists():
        a = models.Authenticator.objects.get(authenticator=auth_value)
        return _success_response(request, {'user_id': a.user_id})
    return _error_response(request, "invalid auth")
    '''
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'authenticator' not in request.POST or 'user_id' not in request.POST:
        return _error_response(request, "missing user_id or authenticator")
    auth_value = request.POST['authenticator']
    user_id = request.POST['user_id']
    if models.Authenticator.objects.filter(user_id=user_id).exists():
        a = models.Authenticator.objects.get(user_id=user_id)
        if a.authenticator == auth_value:
            return _success_response(request, "authenticator is valid")
        return _error_response(request, {'authenticator': auth_value})
    return _error_response(request, "invalid user id")
    '''
	

##The auth created over 24 hours would be considered as "old"
#For doing test right, I am using get...have't figured out when and where this method should be called
def delete_old_auth(request):
    if request.method != 'GET':
        return _error_response(request, "must make POST request")
    time_threhold = datetime.now() - timedelta(days=1)
    if models.Authenticator.objects.exclude(date_created__range=(time_threhold, datetime.now())).exists():
         models.Authenticator.objects.exclude(date_created__range=(time_threhold, datetime.now())).delete()
         return _success_response(request, "Old authenticators are deleted")
    return _error_response(request, "No old auth found")




#delete the authenticator when certain amount ot time passed
#def upate_auth():




    
    











##Written by Nipun
def view_company_JobApplications(request, company_id):
    if  request.method !='GET':
        return _error_response(request, "must make GET request")
    try:
        cur_company = get_object_or_404(models.Company, id=company_id)
        job_application_list = models.JobApplication.objects.all().filter(company=cur_company)
    except models.Company.DoesNotExist:
        return _error_response(request, "company not found")

    return _success_response(request, {'job_application_list': job_application_list})



def view_all_transactions(request):
    all_transactions = models.Transaction.objects.all()
    return JsonResponse({'ok': True, 'transaction_list': all_transactions})



def view_all_buyers(request):
    all_buyers = models.Buyer.objects.all()
    return JsonResponse({'ok': True, 'buyer_list': all_buyers})

def view_all_sellers(request):
    all_sellers = models.Seller.objects.all()
    return JsonResponse({'ok': True, 'seller_list': all_sellers})










def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})

