from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from google.cloud import datastore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .models import CustomUser, metadata
from dialektor_files.fileHandling import DialektFileSecurity, StorageBucket
import hashlib

def login_user(request, second=None):
    # main entry page (aka. login page)
    # The "second" argument is not used here, however, it is needed for the group regex call on urls
    return render(request, 'login.html')

def index_home(request, second=None):
    return render(request, 'home.html')

def render_sound(request, sound_id):
    sound = metadata.objects.get(fileID=sound_id)
    print(sound.title)
    return render(request, 'sound.html', {'sound': sound_id, 'title': sound.title})

def get_sound(request, sound_id):
    meta_obj = metadata.objects.get(fileID=sound_id)
    storage = StorageBucket(meta_obj)
    storage.s_read_file_from_bucket()
    file_rcv = storage.file
    return HttpResponse(file_rcv, content_type='application/force-download')

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
    id = hashlib.md5(str.encode(username+email))
    CustomUser.objects.create_user(username, email, password, first_name=firstName, last_name=lastName, inst_name=instName, inst_addr=instAddr, inst_city=instCity, inst_state=instState, inst_country=instCountry, user_id=id.hexdigest())
    loginInfo = authenticate(username=username, password=password)
    login(request, loginInfo)
    return redirect('/')



def upload(request):
    print(request.POST)
    print(request.FILES)
    title = request.POST.get('title', 'none')
    collection = request.POST.get('collection', 'none')
    category = request.POST.get('category', 'none')
    tags = request.POST.get('tags', 'none')
    length = request.POST.get('length', 'none')
    user = request.user.user_id
    fileID = hash_object = hashlib.md5(str.encode(title+user+collection)).hexdigest()
    file = metadata(user_id=user, title=title,  rec_length=length, collection=collection, category=category, tags=tags, fileID=fileID)
    file.save()
    meta_obj = metadata.objects.get(fileID=fileID)
    storage_bucket = StorageBucket(meta_obj)
    storage_bucket.file = request.FILES['blob'].read()
    storage_bucket.s_write_file_to_bucket()
    del storage_bucket
    storage_bucket2 = StorageBucket(meta_obj)
    storage_bucket2.s_read_file_from_bucket()
    file_rcv = storage_bucket2.file
    return HttpResponseRedirect(reverse('render_sound', kwargs={'sound_id': fileID}))

def signup(request):
    # renders the signup form
    return render(request, 'signup.html')

def profile(request):
    # Renders the profile page


    # Get list of all user recordings
    ## TODO: only list latest 10 recordings
    userId = request.user.user_id
    meta_objs = metadata.objects.filter(user_id=userId)
    records = {}
    for obj in meta_objs:
        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection' : obj.collection,
            'tags' : obj.tags,
        }
        records[obj.fileID] = data

    content = {
    # TODO: get real profile pic name after it gets implemented
    'profile_pic': '/static/defaultprofile1.png',
    'user_records' : records
    }
    return render(request, 'profile.html',content)

def profile_update(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username = request.user.username)
        user.first_name = request.POST.get('first_name','none')
        user.last_name = request.POST.get('last_name','none')
        user.save()
        return HttpResponseRedirect('/profile')

    else:    
        content = {
            # TODO: get real profile pic name after it gets implemented
            'profile_pic': '/static/defaultprofile1.png',
        }
        return render(request, "editUserProfile.html",content)