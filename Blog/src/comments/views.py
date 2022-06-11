from django.shortcuts import render,get_object_or_404
from .forms import CommentForm
from .models import Comment
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# Create your views here.
def comment_thread(request,com_id):
    obj = get_object_or_404(Comment, id=com_id)
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