from django.shortcuts import render
from google.cloud import datastore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your views here.


def login(request, second=None):
    # main entry page (aka. login page)
    # The "second" argument is not used here, however, it is needed for the group regex call on urls
    return render(request, 'login.html')

def index_home(request, second=None):
    return render(request, 'home.html')

def create_user(request):
    print(request.POST)
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    firstName = request.POST['first_name']
    lastName = request.POST['last_name']
    #User.objects.create_user(username, email, password, first_name=firstName, last_name=lastName)
    return render(request, 'signup.html')

def signup(request):
    # renders the signup form
    return render(request, 'signup.html')


