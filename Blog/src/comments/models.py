import re
from tkinter import CASCADE
from tkinter.messagebox import NO
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your models here.

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager,self).filter(parent=None)
        return qs
    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager,self).filter(content_type=content_type,object_id = obj_id).filter(parent=None) #-- super(CommentManager,self) ==> Comments.objects
        return qs

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE) #---Creating a relationship between Post and User # default=1 means superuser
    # post= models.ForeignKey(Post,on_delete=models.CASCADE) #---To Attach the Comment to a Particular Post
    
    #--- Generic Foreign Keys, to attach a comment to any Models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE) #--Parent Comment (Parent is top level and Children are Bottom Level)
    
    content= models.TextField(blank=False,null=False)
    timestamp =models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ["-timestamp"]
        
    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:comment_thread", kwargs={"com_id": self.id})
    
    def get_delete_url(self):
        return reverse("comments:comment_delete", kwargs={"com_id": self.id})

    def children(self): #--Reply Elements (Replies)
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True