"""Dialektor_ URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
import dialektor.views as views

subdomain = 'dialektor/'

urlpatterns = [
    path(subdomain + 'admin/', admin.site.urls),
    path(subdomain + 'accounts/', include('django.contrib.auth.urls')),
    path(subdomain + '', views.index_home, name='home'),
    path(subdomain + 'signup/', views.signup, name="signup"),
    path(subdomain + 'signup/create_user', views.create_user, name="create_user"),
    path(subdomain + 'upload', views.upload, name="upload"),
    path(subdomain + 'sounds/<str:sound_id>/', views.render_sound, name='render_sound'),
    path(subdomain + 'pic/<str:pic_id>/', views.get_picture, name="get pic"),
    path(subdomain + 'raw/<str:sound_id>/', views.get_sound, name="get_sound"),
    path(subdomain + 'download/<str:sound_id>/', views.download_sound, name="download_sound"),
    path(subdomain + 'profile/',views.profile, name="profile"),
    path(subdomain + 'userUpdateProfile/', views.profile_update, name="profile_update"),
    path(subdomain + 'changePassword/', views.change_pass, name="change_pass"),
    path(subdomain + 'collection/<str:collection_name>/', views.collection_list, name="collection_list"),
    path(subdomain + 'tag/<str:tag_name>/', views.tag_list, name="tag_list"),
    path(subdomain + 'profilePic/', views.get_profile_pic, name="get_profile_pic"),

    path(subdomain + 'collections', views.get_collections, name="get_collections"),

    path(subdomain + 'search', views.search, name="search")
]
