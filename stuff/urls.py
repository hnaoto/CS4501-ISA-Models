from django.conf.urls import patterns, include, url
from django.contrib import admin

from stuff import main

urlpatterns = patterns('',
                       url(r'^api/v1/users/create$', main.create_user),
                       url(r'^api/v1/transaction/create$', main.create_transaction),
                       url(r'^api/v1/job-application/create$', main.create_JobApplication),
                       url(r'^api/v1/users/(\d+)$', main.user_lookup),

)
