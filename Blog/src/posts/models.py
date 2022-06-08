from pyexpat import model
import re
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
#--Take Some Action Right Before Model is getting saved
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType



#Model Manager Examples :
# Post.objects.all() , Post.create(user=user,title=title,......)

#--We can override the ModelManagers with our custom function
#--Overriding the Default all
class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

#--Upload images to a specific location inside Media URL
def upload_location(instance,filename):
    print("Instance :: " ,instance)
    return f"images/{filename}"
    
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE) #---Creating a relationship between Post and User # default=1 means superuser
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field") #---Need Pillow Library to Use This Field
    height_field = models.IntegerField(default=0) #--Autodetermines Height of Image
    width_field = models.IntegerField(default=0) #--Autodetermines Width of Image
    content = models.TextField()
    draft = models.BooleanField(default=False) #--For Drafts
    publish = models.DateTimeField(default = None,auto_now=False,auto_now_add=False)  #--For Drafts
    updated = models.DateTimeField(auto_now=True,auto_now_add=False) 
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True) 

    objects = PostManager()

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug":self.slug})
    
    def get_markdown(self): #--This method will return markdown/truncated content to display in the post list
        return mark_safe(markdown(self.content))

    #-- This Property of the instance can be used anywhere
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug = slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{instance.id}"
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

#--- Pre Save will run before everytime a model is getting saved
pre_save.connect(pre_save_post_reciever,sender = Post)
