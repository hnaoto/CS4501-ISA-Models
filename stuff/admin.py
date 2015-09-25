from django.contrib import admin
from stuff.models import User, Company, Transaction, JobApplication

admin.site.register(User, Company, Transaction, JobApplication)