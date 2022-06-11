"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import comment_thread,comment_delete

app_name = "comments" #--Assigning an App Name ensures we can use the same functions in other apps as well
urlpatterns = [
    #-- URLS only Allows Regular Expressions to be applied and not Paths
    url(r'^(?P<com_id>\d+)/$', comment_thread, name='comment_thread'), #---Url Modified to accept Slugs
    url(r'^(?P<com_id>\d+)/delete/$', comment_delete,name='comment_delete'),
]