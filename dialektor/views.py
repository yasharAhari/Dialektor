from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import CustomUser, metadata
from .models import collection as Collection
from dialektor_files.fileHandling import DialektFileSecurity, StorageBucket
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import operator
from functools import reduce
from datetime import datetime


def login_user(request, second=None):
    # main entry page (aka. login page)
    # The "second" argument is not used here, however, it is needed for the group regex call on urls
    return render(request, 'login.html')


def index_home(request, second=None):
    print(request.user)
    if request.user.is_anonymous:
        return render(request, 'home.html')
    elif not request.user.inst_addr == '':  # if this is a researcher
        return render(request, 'researcher.html', {'user_id': request.user.user_id})
    return render(request, 'home.html', {'user_id': request.user.user_id})


def render_sound(request, sound_id):
    sound = metadata.objects.get(fileID=sound_id)
    user = CustomUser.objects.get(user_id=sound.user_id)
    collection = Collection.objects.get(user_id=sound.user_id, name=sound.collection)
    print(sound.title)
    return render(request, 'sound.html',
                  {'sound': sound_id, 'title': sound.title, 'author': user.username, 'pic_src': collection.pic_id})


def get_sound(request, sound_id):
    fs = FileSystemStorage()
    f_data = fs.open(str(sound_id))
    return HttpResponse(f_data.read(), content_type='application/force-download')


def download_sound(request, sound_id):
    fs = FileSystemStorage()
    f_data = fs.open(str(sound_id))
    response = HttpResponse(f_data.read(), content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(sound_id)
    return response


def get_picture(request, pic_id):
    try:
        file_rcv = StorageBucket.read_file_from_storage(pic_id)
    except IOError:
        file_rcv = StorageBucket.read_file_from_storage('defaultCollection.png')
    return HttpResponse(file_rcv, content_type='image/png')


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
    id = hashlib.md5(str.encode(username + email))
    CustomUser.objects.create_user(username, email, password, first_name=firstName, last_name=lastName,
                                   inst_name=instName, inst_addr=instAddr, inst_city=instCity, inst_state=instState,
                                   inst_country=instCountry, user_id=id.hexdigest())
    loginInfo = authenticate(username=username, password=password)
    login(request, loginInfo)
    return redirect('/dialektor/')


def upload(request):
    print(request.POST)
    print(request.FILES)
    print(request.user.user_id)
    title = request.POST.get('title', 'none')
    collection = request.POST.get('collection', 'none')
    category = request.POST.get('category', 'none')
    tags = request.POST.get('tags', 'none')
    length = request.POST.get('length', 'none')
    user = request.user.user_id
    fileID = hash_object = hashlib.md5(str.encode(title + user + collection)).hexdigest()
    file = metadata(user_id=user, title=title, rec_length=length, collection=collection, category=category, tags=tags,
                    fileID=fileID)
    file.save()
    fs = FileSystemStorage()
    fs.save(str(fileID), request.FILES['blob'])
    collections = Collection.objects.all().filter(user_id=user)
    col_name = request.POST.get('collection', 'none')
    names = [collection.name for collection in collections]
    if col_name not in names:
        pic_id = hashlib.md5(str.encode(col_name + user)).hexdigest()
        c = Collection(user_id=user, name=request.POST.get('collection', 'none'), pic_id=pic_id)
        c.save()
        collection_pic = request.FILES.get('collection-pic', None)
        if collection_pic is not None:
            collection_pic.name = pic_id
            StorageBucket.write_file_to_storage(pic_id, collection_pic)
    return HttpResponse(fileID)


def signup(request):
    # renders the signup form
    return render(request, 'signup.html')


def profile(request):
    # check if user is logged in
    # since we are trying to access user information
    if request.user.is_anonymous:
        return HttpResponseRedirect('/dialektor/')

    ## TODO: only list latest 10 recordings

    userId = request.user.user_id

    # Get list of all user recordings, we need all of them for getting tags
    meta_objs = metadata.objects.filter(user_id=userId).order_by('-date_created')

    # All user tags
    tags = set([])

    user_tags = {}

    # records are dic of all user recordings
    records = {}
    for obj in meta_objs:
        # Add the tags in the current record to the list
        for tag in obj.tags.split(','):
            tags.add(tag.strip())

        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection': obj.collection,
            'tags': obj.tags,
        }
        records[obj.fileID] = data

    # get user collections

    collection_list = Collection.objects.filter(user_id=userId)
    collections = {}

    for obj in collection_list:
        data = {
            'picture': obj.pic_id
        }
        collections[obj.name] = data

    # Collect all user tags
    for tag in tags:
        data = {
            'tag_name': tag
        }
        user_tags[tag] = data

    content = {
        # TODO: get real profile pic name after it gets implemented
        'profile_pic': '/static/dialektor/defaultprofile1.png',
        'user_records': records,
        'user_collections': collections,
        'user_tags': user_tags
    }
    return render(request, 'profile/profile.html', content)


def collection_list(request, collection_name):
    # check if user is logged in
    if request.user.is_anonymous:
        return HttpResponseRedirect('/dialektor/')

    user = request.user.user_id

    # check if the collection exist
    try:
        collection = Collection.objects.get(user_id=user, name=collection_name)
    except ObjectDoesNotExist:
        return messenger(request, message="No such collection as " + collection_name, m_type="warning",
                         url_return='/dialektor/profile/')

    # Get list of all user recordings, we need all of them for getting tags
    meta_objs = metadata.objects.filter(user_id=user, collection=collection_name).order_by('-date_created')
    # records are dic of all user recordings
    records = {}
    tags = set([])
    for obj in meta_objs:
        # Add the tags in the current record to the list
        for tag in obj.tags.split(','):
            tags.add(tag.strip())

        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection': obj.collection,
            'tags': obj.tags,
        }
        records[obj.fileID] = data

    user_tags = {}

    # Collect all user tags
    for tag in tags:
        data = {
            'tag_name': tag
        }
        user_tags[tag] = data

    content = {
        'collection_name': collection_name,
        'picture': collection.pic_id,
        'user_records': records,
        'user_tags': user_tags
    }

    return render(request, 'profile/collectionList.html', content)


def tag_list(request, tag_name):
    # check if user is logged in
    if request.user.is_anonymous:
        return HttpResponseRedirect('/dialektor/')

    user = request.user.user_id

    meta_objs = metadata.objects.filter(user_id=user, tags__contains=tag_name).order_by('-date_created')
    if len(meta_objs) == 0:
        return messenger(request, message="No such Tag", m_type="warning", url_return="/dialektor/profile/")

    # records are dic of all user recordings
    records = {}
    for obj in meta_objs:
        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection': obj.collection,
            'tags': obj.tags,
        }
        records[obj.fileID] = data

    content = {
        'tag_name': tag_name,
        'user_records': records
    }
    return render(request, 'profile/tagList.html', content)


def get_user_profile_pic_id(user_info: CustomUser):
    hashed = hashlib.md5(
        str.encode(user_info.email + user_info.username + "picture_salt_1ef88f55e84sf684tht6")).hexdigest()
    print(hashed)
    return hashed


def profile_update(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        user.first_name = request.POST.get('first_name', 'none')
        user.last_name = request.POST.get('last_name', 'none')
        user.save()

        ##profile_pic = request.POST.get('profile-pic', False)
        ##print(request.POST.get('profile-pic', False))
        if request.FILES['profile-pic']:
            pic_file_id = get_user_profile_pic_id(CustomUser.objects.get(username=request.user.username))
            StorageBucket.write_file_to_storage(pic_file_id, request.FILES['profile-pic'].read())

        return messenger(request, message="Changes Saved Successfully!", m_type="success", url_return="/dialektor/profile/")

    else:
        content = {
            # TODO: get real profile pic name after it gets implemented
            'profile_pic': '/static/dialektor/defaultprofile1.png',
        }
        return render(request, "profile/editUserProfile.html", content)


def get_profile_pic(request):
    pic_file_name = get_user_profile_pic_id(CustomUser.objects.get(username=request.user.username))
    print("serving the file " + pic_file_name)
    try:
        file_rcv = StorageBucket.read_file_from_storage(pic_file_name)
        print("There is a profile picture")
    except IOError:
        file_rcv = StorageBucket.read_file_from_storage("defaultprofile1.png")
        print("There is NOT a profile picture")
    return HttpResponse(file_rcv, content_type='application/force-download')


def change_pass(request):
    message = ""
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        entered_pass = request.POST.get('password', False)
        new_pass = request.POST.get('new_password', False)
        if entered_pass is not False:
            # check for current password
            if user.check_password(entered_pass):
                return render(request, 'profile/changePass.html')
            else:
                message = "Password is not correct!"
                return render(request, 'profile/providePass.html', {'message': message})
        else:
            # Change pass word
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, request.user)
            return messenger(request, message="Password successfully updated!", m_type="success", url_return="/dialektor/profile")
    else:
        return render(request, 'profile/providePass.html', {'message': message})
    pass


def messenger(request, message="Hello there", m_type="undefined", url_return="/dialektor/"):
    return render(request, 'profile/messenger.html', {'message': message, 'type': m_type, 'ureturn': url_return})


def get_collections(request):
    collection_list = ""
    user = request.user.user_id
    collections = Collection.objects.all().filter(user_id=user)
    for collection in collections:
        collection_list += collection.name + ", "
    return HttpResponse(collection_list)


def search(request):
    tags = request.POST['tags']
    tags_list = tags.split(',')  # split tags into seprate items
    tags_list = [x.strip(' ') for x in tags_list]
    category = request.POST['category']
    after = request.POST['afterDate']
    before = request.POST['beforeDate']
    useAfter = False
    useBefore = False
    if not after=='':
        useAfter = True
    if not before=='':
        useBefore = True
    sounds = metadata.objects.filter(category__iexact=category).filter(reduce(operator.and_,
                                                                              (Q(tags__icontains=x) for x in
                                                                               tags_list))).order_by('-date_created')  # For now search for items that are in the category and with the tags within the given tags
    sound_list = {}
    tags = set([])
    if useBefore:
        before_dt = datetime.strptime(before, "%m/%d/%Y")
    if useAfter:
        after_dt = datetime.strptime(after, "%m/%d/%Y")
    for obj in sounds:
        # Add the tags in the current record to the list
        obj_dt = datetime.strptime(obj.date_created.__str__()[0:10], "%Y-%m-%d")
        if \
                ((useBefore and useAfter) and obj_dt > after_dt and obj_dt < before_dt) \
                or ((useBefore and not useAfter) and obj_dt < before_dt) \
                or ((useAfter and not useBefore) and obj_dt > after_dt) \
                or (not useAfter and not useAfter):
            for tag in obj.tags.split(','):
                tags.add(tag.strip())

            data = {
                'ID': obj.fileID,
                'date': obj.date_created,
                'tags': obj.tags,
            }
            sound_list[obj.fileID] = data

    return render(request, 'search.html', {'sounds': sound_list.values()})
