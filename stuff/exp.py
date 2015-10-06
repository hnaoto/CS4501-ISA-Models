import os
os.system("pip install -q requests")

# same as  os.system, but more ideomatic
# unable to quiet
# import subprocess
# subprocess.call(["pip","install","-q", "requests"],, stdout=open(os.devnull, 'wb'))

import requests
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django import db
from stuff import models #TODO: import specific models from .models, to prevent having to retype models everytime
from django.core import serializers

from stuff import main

def request(url):
  return requests.get(url)

def http_to_json(url):
  return requests.get(url).json

def all_sellers(request):
  r = requests.get(r'^api/v1/sellers/all/') #TODO: make this URL correct. 
  return r

def all_buyers(request):
  return requests.get(r'^api/v1/buyers/all/')


'''
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

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})
'''