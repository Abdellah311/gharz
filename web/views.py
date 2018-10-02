# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from json import JSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from web.models import Token, User, Kharj, Daramad
from datetime import datetime

# Create your views here.

@csrf_exempt
def sabte_daramad(request):
    """karbar kharji ra sabt mikonad"""

    this_token= request.POST['token']
    this_user= User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date= datetime.now()
    Daramad.objects.create(karbar= this_user, meghdar= request.POST['meghdar'],
    matn= request.POST['matn'],tarikh= date)
    return JsonResponse({
        'status':'ok',
    },encoder= JSONEncoder)


@csrf_exempt
def sabte_kharj(request):
    """karbar kharji ra sabt mikonad"""

    this_token= request.POST['token']
    this_user= User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date= datetime.now()
    Kharj.objects.create(karbar= this_user, meghdar= request.POST['meghdar'],
    matn= request.POST['matn'],tarikh= date)
    return JsonResponse({
        'status':'ok',
    },encoder= JSONEncoder)
