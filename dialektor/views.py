from django.shortcuts import render

# Create your views here.


def index_home(request, second=None):
    # main entry page (aka. login page)
    # The "second" argument is not used here, however, it is needed for the group regex call on urls
    return render(request, 'login.html')


def signup(request):
    # renders the signup form
    return render(request, 'signup.html')
