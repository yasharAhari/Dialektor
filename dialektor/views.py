from django.shortcuts import render, redirect
from google.cloud import datastore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .models import CustomUser, metadata
import hashlib

def login_user(request, second=None):
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
    instName = request.POST['institution_name']
    instAddr = request.POST['institution_address']
    instCity = request.POST['institution_city']
    instState = request.POST['institution_state']
    instCountry = request.POST['institution_country']
    CustomUser.objects.create_user(username, email, password, first_name=firstName, last_name=lastName, inst_name=instName, inst_addr=instAddr, inst_city=instCity, inst_state=instState, inst_country=instCountry)
    loginInfo = authenticate(username=username, password=password)
    login(request, loginInfo)
    return redirect('/')


def upload(request):
    title = request.POST['title']
    collection = request.POST['collection']
    category = request.POST['category']
    tags = request.POST['tags']
    length = request.POST['length']
    user = request.user.username
    fileID = hash_object = hashlib.md5(str.encode(title+user+length)).hexdigest()
    file = metadata(user_id=user, title=title,  rec_length=length, collection=collection, category=category, tags=tags, fileID=fileID)
    file.save()
    return redirect('/')

def signup(request):
    # renders the signup form
    return render(request, 'signup.html')
