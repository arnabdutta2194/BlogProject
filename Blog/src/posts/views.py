from django.db.models.query_utils import Q
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm


# List All Posts View
def post_list(request):
    # return HttpResponse("<h1>List</h1>")
    #--Rendering a Template : Parameters : Request -- Template Path -- Context
    #-- Context is passed as a dictionary to HTML
    querySet = Post.objects.all()
    
    # instance = Post.objects.get(id=6) #-- This will throw error is ID is not found
    #-- Django provides a better way to handle this using get_object_or_404
    # instance = get_object_or_404(Post,id=1)
    # instance = get_object_or_404(Post,title = "FB Post")

    if request.user.is_authenticated:
        context = {
            "title" : "User Is Authenticated",
            "objects_list" : querySet
        }
    else:
        context = {
            "title" : "User Is Not Authenticated",
            "objects_list" : querySet
        }
        
    return render(request,"posts/index.html",context) 

# Create A Post View
def post_create(request):
    #--- The Below is not a Good Practice
    # form = PostForm()
    # if request.method == "POST": 
    #     print(request.POST) #--- Will Send a Key-Pair Query Dictionary : <QueryDict: {'csrfmiddlewaretoken': ['RbDA2E0G6ajmp2WqSDofJBSC01uJBdJJ2drZ7plq3iKS3ViVu9T0PsKXDKPwseUa'], 'title': ['Title'], 'content': ['Content']}>
    #     print(request.POST.get("title"))
    #     print(request.POST.get("content"))
    #     title = request.POST.get("title")
    #     content = request.POST.get("content")
    #     Post.objects.create(title=title,content=content)
    
    #--- Best Practice when Using Model Forms
    form = PostForm(request.POST or None)
    if form.is_valid(): #--Model Form Validations
        instance = form.save(commit=False)
        instance.save()
        print(form.cleaned_data.get("title"))
    context = {
        "form":form
    }    
    return render(request,"posts/post_create.html",context) 


# Check Post Detail
def post_detail(request,id=None):
    # instance = get_object_or_404(Post,title = "FB Post")
    instance = get_object_or_404(Post,id=id)
    context = {
        "title" : instance.title,
        "instance" : instance,
    }
    return render(request,"posts/post_detail.html",context) 


# Update Existing Post
def post_update(request):
    return HttpResponse("<h1>Update</h1>")

# Delete a Post
def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")