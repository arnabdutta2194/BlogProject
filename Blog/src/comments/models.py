from tkinter import CASCADE
from django.db import models
from django.conf import settings
from posts.models import Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE) #---Creating a relationship between Post and User # default=1 means superuser
    # post= models.ForeignKey(Post,on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content= models.TextField(blank=False,null=False)
    timestamp =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)