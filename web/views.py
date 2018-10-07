# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import requests
import json
from django.http import JsonResponse
from json import JSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from web.models import Token, User, Kharj, Daramad, Passwordresetcodes
from datetime import datetime
from django.contrib.auth.hashers import make_password
from postmark import PMMail
import string,time,random

# Create your views here.

random_str= lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase +string.digits))
def index(request):
    context= {}
    return render(request, 'index.html', context)
def get_client_ip(request):
    x_forwarded_for= request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip= x_forwarded_for.split(',')[0]
    else:
        ip= request.META.get('REMOTE_ADDR')
        return ip
def grecaptcha_verify(request):
    data= request.POST
    captcha_rs= data.get('g-recaptcha-response')
    url= "https://www.google.com/recaptcha/api/siteverify"
    params= {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs= requests.get(url, params= params,verify= True)
    verify_rs= verify_rs.json()
    return verify_rs.get('success',False)

def register(request):
    if request.POST.has_key('requestcode'): #form por shode. agar spam nabashe, code sakhte va dar database zakhire mishe, vase taeide email sabr mikone
        #check recaptcha
        if not grecaptcha_verify(request): #captcha sahih nabud
            context= {'message':'لطفا دوباره وارد کنید کد یا تشخیص عکس درست نبود.'}
            return render(request,'register.html',context)
        if User.objects.filter(email= request.POST['email']).exists():
            context= {'message':'این ایمیل قبلا ثبت شده!!اگر ایمیل خود را فراموش کرده اید از قسمت فراموشی پسورد آن را بازیابی کنید.'}
            return render(request,'register.html',context)
        if not User.objects.filter(username= request.POST['username']).exists(): #agar user mogood nabud
            code= random_str(28)
            now= datetime.now()
            email= request.POST['email']
            password= make_password(request.POST['password'])
            username= request.POST['username']
            temporarycode= Passwordresetcodes(email= email, time= now, code= code, username= username, password= password)
            temporarycode.save()
            message= PMMail(api_key= settings.POSTMARK_API_TOKEN,
                            subject= 'فعالسازی حساب کثیر',
                            sender= 'abfani90@gmail.com',
                            to= email,
                            text_body= "برای فعالسازی حساب کثیر خود روی لینک روبرو کلیک کنید {}?email={}$code={}".format(request.build_absolute_uri('/accounts/register'), email, code),
                            tag= "account request")
            message.send()
            context= {'message', 'لینک فعالسازی حساب به ایمیل شما فرستاده شده است لطفا ایمیل خود را چک کنید.'}
            return render(request,'login.html',context)
        else:
            context= {'message':'از نام کاربری دیگری استفاده کنید'}
            return render(request,'register.html',context)

    elif request.GET.has_key('code'):
        email= request.POST['email']
        code= request.POST['code']
        if Passwordresetcodes.objects.filter(code=code).exists():
            new_temp_user= Passwordresetcodes.objects.get(code=code)
            newuser= User.objects.create(username= new_temp_user.username, password= new_temp_user.password, email= email)
            this_token= random_str(48)
            token= Token.objects.create(user= newuser, token= this_token)
            Passwordresetcodes.objects.filter(code=code).delete()
            context= {'message':'اکانت فعال شد لاگین کنید توکن شما {} است'.format(this_token)}
            return render(request,'login.html',context)
        else:
            context= {'message':'کد فعالسازی معتبر نیست دوباره تلاش کنید'}
            return render(request,'login.html',context)
    else:
        context= {'message': ''}
        return render(request,'register.html',context)




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
