import re
from termios import INPCK
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

def login_view(request):
    title = "Login"
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password) #-- First we need to Authenticate a User
        login(request,user) #-- Once a user is authenticated, after that it can login
        print(request.user.is_authenticated)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request,"form.html",{"form":form,"title":title})

def register_view(request):
    title  = "Register"
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    context = {
        "form" : form,
        "title" : title,
    }

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request,new_user)
        if next:
            return redirect(next)
        return redirect("/")

    return render(request,"form.html",context)

def logout_view(request):
    logout(request)
    return redirect("/")


