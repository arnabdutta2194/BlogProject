from django.db.models.query_utils import Q
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post


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
    return HttpResponse("<h1>Create</h1>")

# Check Post Detail
def post_detail(request):
    instance = get_object_or_404(Post,title = "FB Post")
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