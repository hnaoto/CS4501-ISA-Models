from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from stuff import main

urlpatterns = patterns('',
                       
                       
                       
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/v1/users/create$', main.create_user),
                       url(r'^api/v1/transaction/create$', main.create_transaction),
                       url(r'^api/v1/company/create$', main.create_company),
                       url(r'^api/v1/job-application/create$', main.create_JobApplication),
                       url(r'^api/v1/users/(\d+)$', main.lookup_user),
                       url(r'^api/v1/sellers/all$', main.all_sellers),
                       url(r'^api/v1/buyers/all$', main.all_buyers),
                       
                       

)


urlpatterns += staticfiles_urlpatterns()

