from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q
from comments.models import Comment


# List All Posts View
def post_list(request):
    today = timezone.now().date()
    # return HttpResponse("<h1>List</h1>")
    #--Rendering a Template : Parameters : Request -- Template Path -- Context
    #-- Context is passed as a dictionary to HTML
    posts_list = Post.objects.active().order_by("-timestamp") #--Ignoring Draft and Future Pots
    if request.user.is_staff or request.user.is_superuser:   #--Showing Draft and Future Pots to Staffs and Superusers
        posts_list = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    # instance = Post.objects.get(id=6) #-- This will throw error is ID is not found
    #-- Django provides a better way to handle this using get_object_or_404
    # instance = get_object_or_404(Post,id=1)
    # instance = get_object_or_404(Post,title = "FB Post")
    paginator = Paginator(posts_list, 3) # Show 10 Posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        context = {
            "title" : "All Posts",
            "objects_list" : posts_list,
            'page_obj': page_obj,
            "today" : today,
        }
    else:
        context = {
            "title" : "All Posts",
            "objects_list" : posts_list,
            'page_obj': page_obj,
            "today" : today,

        }
        
    return render(request,"posts/post_list.html",context) 




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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid(): #--Model Form Validations
        instance = form.save(commit=False)
        instance.save()
        instance.user = request.user
        print(form.cleaned_data.get("title"))
        messages.success(request,"Post Created Successfully")
        return HttpResponseRedirect(reverse_lazy("posts:detail",args=[instance.slug])) #--- Will Redirect to /posts/list
    else:
        messages.error(request,"Post not Created successfully")
    context = {
        "form":form
    }    
    return render(request,"posts/post_create.html",context) 


# Check Post Detail
def post_detail(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # instance = get_object_or_404(Post,title = "FB Post")
    instance = get_object_or_404(Post,slug=slug)
    share_string = quote_plus(instance.content) #--Encoding Content for Social Share Links
    #--Fetching Comments made for Specific Model
    comments = instance.comments #---As it is now a Property
    print(comments)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string, #--Encoded text for Social Shareable Links
        "comments" : comments,
    }
    return render(request,"posts/post_detail.html",context) 


# Update Existing Post
def post_update(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    #-- request.FILES asks for Files Data from Request
    form = PostForm(request.POST or None,request.FILES or None,instance=instance) #--instance=instance will show us the filled form with previous data
    if form.is_valid(): #--Model Form Validations
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        print(form.cleaned_data.get("title"))
        messages.success(request,"Post Updated Successfully")
        return HttpResponseRedirect(reverse_lazy("posts:detail",args=[instance.slug])) #--- Will Redirect to /posts/list
    else:
        messages.error(request,"Post not Updated successfully")
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form":form
    }    
    return render(request,"posts/post_create.html",context) 


# Delete a Post
def post_delete(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,"Post Deleted Successfully")
    return redirect("posts:list")
    