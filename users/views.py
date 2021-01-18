from django.contrib.auth import login, authenticate, logout
from django.contrib import auth
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import SignUpForm,ProfileCReationForm,Mobile_no_Form,Otp_form,ChangePassword
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from .models import OTP
import random
import math
from twilio.rest import Client
import os
from decouple import config


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('Home')

def sign_up(request):
    form = SignUpForm()
    return render(request,'users/signup.html',{
        "form" : form,
        "page":"sign up"
    })

def createuser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user  = authenticate(username = user.username ,password=raw_password)
            auth.login(request,user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,
            'token':token_generator.make_token(user)})
            acttivate_url = 'http://'+domain+link
            email_subject = 'Activate Your account'
            email_body = 'Hi'+user.username+'Please use this link to verify your account.\n'+acttivate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'prand234@gmail.com',
                [user.email]

            )
            email.send(fail_silently=True)
            return render(request,'users/activate_email.html',{
                "username":user.username,
                'page':"activate"
            })
    else:
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form,"page":"signu up"})

class Verification_view(View):
      def get(self,request,uidb64,token):
          return redirect('profile_fillup')

def profile(request):
    return render(request,'users/profile_create.html',{
        "message":"email verified",
        "form":ProfileCReationForm()
    })
def login(request):
    
    return render(request,'users/login.html',{
        "page":"login"
    })
    
def handle_login(request):
    if request.method == "POST":
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username = username,password=raw_password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('index')
        else:
            return HttpResponse("invalid credentials")
    else:
        return HttpResponse("not allowed")

def logout(request):
    auth.logout(request)
    return redirect('Home')

def createprofile(request):
    if request.method == "POST":
       form = ProfileCReationForm(request.POST)
       if form.is_valid():
           request.user.profile.reg_no = form.cleaned_data.get('reg_no')
           request.user.profile.Branch = form.cleaned_data.get('Branch')
           request.user.profile.Year = form.cleaned_data.get('Year')
           request.user.save()
           
           return redirect('Home')

def forgotPassword(request):
    return render( request,'users/forgotpassword.html',{
        'user':request.user,
        'page':'forgotPassword',
        'form':Mobile_no_Form(),
        'message':'nootp'
    })

def send_otp(request):
    if request.method == "POST":
      form = Mobile_no_Form(request.POST)
      if form.is_valid():
         username = form.cleaned_data.get('username')
         mobile_no = form.cleaned_data.get('mobile_no')
         print(mobile_no)
         user = User.objects.get(username = username)
         print(user.password)
         ## generating OTP
         digits = "0123456789"
         otp= ""
         # length of password can be chaged 
         # by changing value in range 
         for i in range(4) : 
           otp += digits[math.floor(random.random() * 10)]
         OTP.objects.create(user=user,otp=otp)
         
         #Sending OTP on email
         email_subject = 'One Time Password'
         email_body = 'Hi '+user.username+'.\nThis is your ONE TIME PASSWORD do not share it with anyone.\n'+otp
         email_ = EmailMessage(
                email_subject,
                email_body,
                'prand234@gmail.com',
                [user.email]
            )
         email_.send(fail_silently=True)

         #Sending OTP on mobile
         account_sid = config('TWILIO_ACCOUNT_SID')
         auth_token = config('TWILIO_AUTH_TOKEN')
         client = Client(account_sid, auth_token)
         message = client.messages.create(
             body=email_body,
             from_='+12053468877',
             to='+91'+mobile_no
         )
         print(message.sid)
         return render( request,'users/enterotp.html',{
        'username':username,
        'page':'forgotPassword',
        'form':Otp_form(),
        'message':'otp'
        })

    else:
        return render( request,'users/forgotpassword.html',{
        'user':request.user,
        'page':'forgotPassword',
        'form':Mobile_no_Form(),
        'message':'nootp'
        })


def check_otp(request):
    username = request.POST['username']
    user = User.objects.get(username = username)
    if request.method == "POST":
       form = Otp_form(request.POST)
       if form.is_valid():
          otp = form.cleaned_data.get('otp')
          
          real_otp = OTP.objects.get(user = user)
          
          print(user.password)
          if otp == real_otp.otp:
               real_otp.delete()
               return render(request,'users/changepassword.html',{
                   'form':SetPasswordForm(user = user),
                   'message':'Otp verified successfully',
                   'username':username,
                   'page':'change password',
               })
               
             
          else:
              return render( request,'users/enterotp.html',{
                     'username':user.username,
                     'page':'forgotPassword',
                     'form':Otp_form(),
                     'message':'otp',
                     'error_message':"Please enter correct otp!!!!"
                    })
       else:
           return render( request,'users/enterotp.html',{
                     'username':user.username,
                     'page':'forgotPassword',
                     'form':Otp_form(),
                     'message':'otp',
                     'error_message':"Please enter valid details"
                    })

    

    

def change_password(request):
    username = request.POST['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
       form = SetPasswordForm(user = user,data = request.POST)
       if form.is_valid():
          
          form.save()
          
          return render(request,'users/passwordc.html',{
              'message':"Password changed successfully!",
              'page':'password changed'
          })
       else:
          return render(request,'users/changepassword.html',{
                 'page':'change_password',
                 'user':user,
                 'message':'OTP Verified successfully',
                 'form':SetPasswordForm(user=user),
                 'username':user.username,
                 'error_message':'fill valid details'
             })
    else:
        return render(request,'users/changepassword.html',{
                 'page':'change_password',
                 'user':user,
                 'message':'OTP Verified successfully',
                 'form':SetPasswordForm(user=user),
                 'username':user.username,
                 'error_message':'fill valid details'
             })
             