from django.shortcuts import render

# Create your views here.


def index_home(request):
    # main entry page (aka. login page)
    return render(request, 'login.html')