from django.shortcuts import render
from django.http import HttpResponse


# List All Posts View
def post_list(request):
    # return HttpResponse("<h1>List</h1>")
    #--Rendering a Template : Parameters : Request -- Template Path -- Context
    return render(request,"posts/index.html",{}) 

# Create A Post View
def post_create(request):
    return HttpResponse("<h1>Create</h1>")

# Check Post Detail
def post_detail(request):
    return HttpResponse("<h1>Detail</h1>")

# Update Existing Post
def post_update(request):
    return HttpResponse("<h1>Update</h1>")

# Delete a Post
def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")