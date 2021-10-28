"""putatoe_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from services.views import home
from users.views import contact,signup,activate,user_login,user_logout,passwordReset,password_reset_confirm,resend_link

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name = 'home'),
    path('contact/',contact),
    path('users/',include('users.urls')),
    path('signup/',signup,name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/',activate, name='activate'),
    path('login/',user_login, name = 'login' ),
    path('logout/',user_logout),
    path('password_reset/',passwordReset, name='password_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/',password_reset_confirm, name= 'password_reset_confirm'),
    path('resend_link/',resend_link,name = "resend_link")
   ]
