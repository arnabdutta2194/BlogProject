from multiprocessing import context
from urllib import response
from django.shortcuts import render,get_object_or_404
from .forms import CommentForm
from .models import Comment
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


# Create your views here.

def comment_delete(request,com_id):
    # obj = get_object_or_404(Comment,id=com_id)
    try:
        obj = Comment.objects.get(id=com_id)
    except:
        raise Http404
    if obj.user != request.user:
        # messages.warning(request,"You do not have permission to view this")
        response_delete = HttpResponse("You do not have permission to delete this")
        response_delete.status_code = 403
        return response_delete
    
    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url() #-- Absolute URL of Parent Post
        obj.delete()
        messages.success(request,"Comment has been deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = { "object" : obj}
    return render(request,"confirm_delete.html",context)

def comment_thread(request,com_id):
    # obj = get_object_or_404(Comment, id=com_id)
    try:
        obj = Comment.objects.get(id=com_id)
    except:
        raise Http404
    if obj.user != request.user:
        messages.warning(request,"You do not have permission to view this")
        raise Http404
    if not obj.is_parent : 
        obj = obj.parent
    content_object = obj.content_object #-- Post That the Comment is on
    # content_id = obj.content_object.id
    initial_data = {
        "content_type" : content_object.get_content_type,
        "object_id" :  obj.object_id
    }
    print(initial_data)
    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        print(form.cleaned_data)
        # c_type = form.cleaned_data.get("content_type") 
        # print(c_type)
        content_type = ContentType.objects.get_for_model(content_object)
        # content_type = ContentType.objects.get_for_model(model=c_type)
        print(content_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id")) #--- To get the Parent Comment ID from Request
        except: 
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj  = parent_qs.first()
        print("parent_id",parent_id)
        print("parent_obj",parent_obj)
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type= content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj
        )

        if created:
            messages.success(request,"Comment Successfully Created")
        print("Content Object")
        print(new_comment.content_object)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context ={
        "comment" : obj,
        "comment_form" : form
    }
    return render(request,"comment_thread.html", context)