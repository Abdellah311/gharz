# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Passwordresetcodes(models.Model):
    code= models.CharField(max_length=32)
    email= models.CharField(max_length=120)
    time= models.DateTimeField()
    username= models.CharField(max_length=50)
    password= models.CharField(max_length=50)

class Token(models.Model):
    user=  models.OneToOneField(User, on_delete=models.CASCADE)
    token= models.CharField(max_length= 48)
    def __unicode__(self):
        return "{}_Token".format(self.user)

class Kharj(models.Model):
    matn= models.CharField(max_length=300)
    tarikh= models.DateTimeField()
    meghdar= models.BigIntegerField()
    karbar= models.ForeignKey(User)
    def __unicode__(self):
        return "{}-{}-{}".format(self.tarikh,self.karbar,self.meghdar)
class Daramad(models.Model):
    matn= models.CharField(max_length=300)
    tarikh= models.DateTimeField()
    meghdar= models.BigIntegerField()
    karbar= models.ForeignKey(User)
    def __unicode__(self):
        return "{}-{}-{}".format(self.tarikh,self.karbar,self.meghdar)
