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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index_home, name='home'),
    path('signup/', views.signup),
    path('signup/create_user', views.create_user),
    path('upload', views.upload),
    path('sounds/<str:sound_id>/', views.render_sound, name='render_sound'),
    path('pic/<str:pic_id>/', views.get_picture, name="get pic"),
    path('raw/<str:sound_id>/', views.get_sound, name="get_sound"),
    path('download/<str:sound_id>/', views.download_sound, name="download_sound"),
    path('profile/',views.profile, name="profile"),
    path('userUpdateProfile/', views.profile_update, name="profile_update"),
    path('changePassword/', views.change_pass, name="change_pass"),
    path('collection/<str:collection_name>/', views.collection_list, name="collection_list"),
    path('tag/<str:tag_name>/', views.tag_list, name="tag_list"),
    path('profilePic/', views.get_profile_pic, name="get_profile_pic"),

    path('collections', views.get_collections, name="get_collections"),

    path('search', views.search, name="search")
]
