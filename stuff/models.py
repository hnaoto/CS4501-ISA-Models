import datetime
from django.db import models
from django.utils import timezone

#top-level model for website user
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=96)
    usertype = models.CharField(max_length=6) #TODO: instead of usertype field, have links to both buyer and seller profile and check each time to see if profile in question exists
    def __str__(self):
        return self.username

#profile for each company on recruiting platform
class Company(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField(max_length=500)
    def __str__(self):
        return self.name

#users seeking a job referral
class Buyer(models.Model):
    #username = models.CharField(max_length=50, unique=true)
    resume_url = models.URLField(max_length=200)
    user_account = models.ForeignKey(User, unique=True)
    def __str__(self):
        return self.user_account

#users offering job referrals for a specific company
class Seller(models.Model):
    company = models.OneToOneField(Company)
    user_account = models.ForeignKey(User, unique=True)
    def __str__(self):
        return self.user_account

#when a buyer submits a job application and a seller accepts it, a transaction is created
class Transaction(models.Model):
    #buyer = models.ForeignKey(buyer)
    #seller = models.ForeignKey(Seller)
    buyer= models.OneToOneField(Buyer)
    seller = models.OneToOneField(Seller)
    timestamp = models.DateTimeField(default=timezone.now)
    negotiation = models.TextField(max_length=1000)
    def __str__(self):
        return str(self.negotiation)

#when a buyer is interested in a company, they submit a job application which any seller can see if they belong to the company which the buyer applied too
class JobApplication(models.Model):
    #company = models.ForeignKey(Company, unique=true)
    company = models.OneToOneField(Company)
    buyer = models.OneToOneField(Buyer)
    greeting = models.CharField(max_length=256)
    detail = models.TextField(max_length=1000)
    def __str__(self):
        return str(self.greeting)
  
#written by Trintiy
class Authenticator(models.Model):
    user_id = models.IntegerField()
    authenticator = models.CharField(max_length=256)
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user_id)
    
    
