from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from stuff import main

urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/v1/users/create$', main.create_user),
                       url(r'^api/v1/buyers/all$', main.all_buyers),
                       url(r'^api/v1/sellers/all$', main.all_sellers),
                       url(r'^api/v1/transaction/create$', main.create_transaction),
                       url(r'^api/v1/transaction/all$', main.view_all_transactions),
                       url(r'^api/v1/company/create$', main.create_company),
                       url(r'^api/v1/job-application/create$', main.create_JobApplication),
                       url(r'^api/v1/job-application/view/(\d+)$', main.view_company_JobApplications),
                       url(r'^api/v1/users/(\d+)$', main.lookup_user),
                       url(r'^api/v1/auth/login$', main.log_in),
                       url(r'^api/v1/auth/logout$', main.log_out),
                       url(r'^api/v1/auth/verify$', main.check_auth),
                       url(r'^api/v1/auth/delete_old_auth$', main.delete_old_auth),
                       url(r'^api/v1/auth/note/create$', main.create_note),
                       

)

urlpatterns += staticfiles_urlpatterns()
