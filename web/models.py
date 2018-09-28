# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
class kharj(models.Model):
    matn= models.CharField(max_length=300)
    tarikh= models.DateTimeField()
    meghdar= models.BigIntegerField()
    karbar= models.ForeignKey(User)
    """docstring for kharj models.Model__
    text= models.charField(max_length=300)
    date= models.DateTimefield()
    (self, arg):
        super(kharj_models.Model()
        text= models.charField(max_length=300)
        date= models.DateTimefield()

        self.arg = arg

# Create your models here."""
