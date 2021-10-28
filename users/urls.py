from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from users.views import signup,activate


urlpatterns = [
    url('admin/', admin.site.urls),
    
]