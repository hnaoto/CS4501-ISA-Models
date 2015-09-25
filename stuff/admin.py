from django.contrib import admin
from stuff.models import User, Company, Buyer, Seller, Transaction, JobApplication

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Company)
admin.site.register(Transaction)
admin.site.register(JobApplication)