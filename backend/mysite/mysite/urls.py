"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", api.api_test),
    path("login/", api.api_login),
    path("register/", api.api_register),
    path("getuserinfo/", api.api_getuserinfo),
    path("changeuserinfo/", api.api_changeuserinfo),
    path("addclass/", api.api_addclass),
    path("getclassinfo/", api.api_getclassinfo),
    path("changeclassinfo/", api.api_changeclassinfo),
    path("deleteclass/", api.api_deleteclass),
    path("arrangeclass/", api.api_arrangeclass),
    path("addclassroom/", api.api_addclassroom),
    path("getclassroominfo/", api.api_getclassroominfo),
    path("mddifyclassroominfo/", api.api_modifyclassroominfo),
    path("deleteclass/", api.api_deleteclass),
    path("getarrangeclasshistory/", api.api_getarrangeclasshistory),
    path("selectcourse/", api.api_selectcourse),
]
