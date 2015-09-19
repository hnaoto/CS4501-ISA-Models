import datetime
from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=50, unique=true)
    password = models.CharField(max_length=96)
    usertype = models.CharField(max_length=6)


class Company(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField(max_length=500)



class Buyer(models.Model):
    #username = models.CharField(max_length=50, unique=true)
    resume_url = models.URLField(max_length=200)
    user_account = models.ForeignKey(User, unique=true)


class Seller(models.Model):
    company = models.OneToOneField(Company)
    user_account = models.ForeignKey(User, unique=true)



class Transaction(models.Model):
    #buyer = models.ForeignKey(buyer)
    #seller = models.ForeignKey(Seller)
    buyer= models.OneToOneField(Buyer)
    seller = models.OneToOneField(Seller)
    timestamp = models.DateTimeField(default=timezone.now)
    negotiation = models.TextField(max_length=1000)


class JobApplication(models.Model):
    #company = models.ForeignKey(Company, unique=true)
    company = models.OneToOneField(Company)
    buyer = models.OneToOneField(Buyer)
    greeting = models.CharField(max_length=256)
    detail = models.TextField(max_length=1000)