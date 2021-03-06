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
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (login_view,register_view,logout_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    #--Direct Path - <appname>.views.<function_name>
    path(r'posts/', include("posts.urls"),name="posts"),  #-- Anythings comes as posts/ - redirect it to urls.py of Posts Application
    path(r'api/posts/', include("posts.api.urls"),name="posts-api"),  #-- Anythings comes as api/posts/ - redirect it to urls.py of posts/api Application
    path(r'comments/', include("comments.urls"),name="comments"),  #-- Anythings comes as posts/ - redirect it to urls.py of Posts Application
    path(r'login/', login_view, name="login"),
    path(r'logout/', logout_view, name="logout"),
    path(r'register/', register_view, name="register"),
    path(r'', include("posts.urls"),name="posts"),  #-- Anythings comes as / - redirect it to urls.py of Posts Application
]
#--- The blow configuration is done to serve Static File During Development
#--- It is not a good practice for Production. In production generally files are served from Cloud
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)