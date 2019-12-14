from django.shortcuts import render

# Create your views here.


def index_home(request, second):
    # main entry page (aka. login page)
    return render(request, 'login.html')


def signup(request):
    # renders the signup form
    return render(request, 'signup.html')
