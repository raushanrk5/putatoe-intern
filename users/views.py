from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import login,authenticate,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import datetime,date,timedelta
from .forms import RegisterForm
from .models import User,Session
import bcrypt

# Token generating function
import random
import string
def TokenGenerator(stringLength:30):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

# Contact page view
def contact(request):
    if request.session.has_key('login_token'):
        context = {"contact":"contact"}
        return render(request,'contact.html',context)
    else:
        return HttpResponse('you have to be logged in to go to this page')

# User Registration views
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            token = TokenGenerator(30)
            mobile_no = form.cleaned_data.get('mobile_no')
            password = form.cleaned_data.get('password')
            password1 = form.cleaned_data.get('password_repeat')
            password_encode = password.encode('utf-8')
# Hashing password
            enc_password = bcrypt.hashpw(password_encode,bcrypt.gensalt())
            bcrypt.checkpw(password_encode, enc_password)
            global to_email
            to_email = form.cleaned_data.get('email')
            status = False
            user = User(username = mobile_no, email=to_email, password=enc_password.decode('utf-8'), authtoken=token, status = status)
            user.save()
            current_site = get_current_site(request)
# Sending activation Email
            mail_subject = 'Activate your Putatoe account.'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            form = RegisterForm()
            context = {'form': form,"password": password, "password1": password1}
            return render(request, 'signup.html',context)
        else:
            if User.objects.filter(email = email).exists():
                registered = True
                form = RegisterForm()
                return render(request, 'signup.html', {'form': form,'registered':registered})

    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

# Verifying and Activating user account
def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
# User account activation session
    created_time = user.created_date.time()
    current_time = datetime.now().time()
    time_diff = datetime.combine(date.today(),current_time) - datetime.combine(date.today(),created_time)
    session = int((time_diff.seconds)/60)
    if user.authtoken == token and session <= 10:
        user.status = True
        user.save()
        return redirect('login')
    elif session > 10:
        return HttpResponse('Your session has expired, please try again.')
    else:
        return HttpResponse('Activation link is invalid!')

# User login view
def user_login(request):
    if request.session.has_key('login_token'):
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
# Checking if user is registered or not
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email = email)
# checking if user is activated or not
                if user.status == True:
                    hashed_password = (user.password).encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'),hashed_password):
                        login_token = TokenGenerator(30)
# Creating user login session
                        session = Session(token=login_token, expire_date=datetime.now() + timedelta(days=15))
                        session.save()
                        request.session['login_token'] = login_token
                        request.session.set_expiry(1296000)  # setting session expiry of 15 days in seconds
                        if request.session.has_key('login_token'):
                            return render(request,'index.html',{'log':'Logout','url':'/logout/'})
                        else:
                            return HttpResponse('session is not there')
                    else:
                        context = {"res": bcrypt.checkpw(password.encode('utf-8'),hashed_password)}
                        return render(request, 'login.html', context)
                else:
                    context = {"status": user.status}
                    return render(request, 'login.html', context)
            else:
                context = { "registered" : User.objects.filter(email=email).exists()}
                return render(request, 'login.html', context)
    context = {"login":"login"}
    return render(request,'login.html',context)

# user logout functionality
def user_logout(request):
    if request.session.has_key('login_token'):
        del request.session['login_token']
        return redirect ('home')
    else:
        return HttpResponse("First, you have to log in")

# Forgot password functionality
def passwordReset(request):
    if not request.session.has_key('login_token'):
        if request.method == 'POST':
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.status = False
                user.save()
# Sending password reset email
                token = user.authtoken
                current_site = get_current_site(request)
                mail_subject = 'Reset your account password'
                message = render_to_string('reset_ps_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
                email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                email.send()
    context = {'Heading':'Forgot Password','modal':'Please confirm your email address to reset your password'}
    return render(request,'password_reset.html',context)

# Confirming user and changing user's password
def password_reset_confirm(request,uidb64,token):
    if User.objects.filter(authtoken=token).exists():
        user = User.objects.get(authtoken=token)
        user.status = True
        user.save()
        if request.method == 'POST':
# Validating and resetting password
            password = request.POST.get('password')
            rePassword = request.POST.get('password_repeat')
            print(password,rePassword)
            if password == rePassword:
                enc_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user.password = enc_password.decode('utf-8')
                user.save()
                return redirect('login')
        context = {"": ""}
        return render(request, 'reset_ps_confirm.html', context)
    else:
        return HttpResponse('password reset link is invalid!')

# Resend activation link again functioality
def resend_link(request):
    if not request.session.has_key('login_token'):
        if request.method == 'POST':
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.created_date = datetime.now()
                user.save()
# resending activation link on user's email
                token = user.authtoken
                current_site = get_current_site(request)
                mail_subject = 'Activate your Putatoe account'
                message = render_to_string('activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
                email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                email.send()
    context = {'Heading':'Resend Link','modal':'Please confirm your email address to complete the registration'}
    return render(request,'password_reset.html',context)


