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
'''
def request(url):
  return requests.get(url)

def http_to_json(url):
  return requests.get(url).json
'''
def all_sellers(request):
  r = requests.get(localhost:8001/api/v1/sellers/all/') #TODO: make this URL correct. 
  return r

def all_buyers(request):
  return requests.get(localhost:8001/api/v1/buyers/all/')
