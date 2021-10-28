from django.shortcuts import render

# Create your views here.
def home(request):
    context={
        'header' : 'Home',
        'log' : 'Login',
        'url': '/login/',
    }
    return render(request, "index.html", context)
