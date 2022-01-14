from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
#--Take Some Action Right Before Model is getting saved
from django.utils.text import slugify
#--Upload images to a specific location inside Media URL
def upload_location(instance,filename):
    return f"{instance.id}/{filename}"
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field") #---Need Pillow Library to Use This Field
    height_field = models.IntegerField(default=0) #--Autodetermines Height of Image
    width_field = models.IntegerField(default=0) #--Autodetermines Width of Image
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True,auto_now_add=False) 
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True) 

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug":self.slug})



def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug = slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug} - {instance.id}"
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

#--- Pre Save will run before everytime a model is getting saved
pre_save.connect(pre_save_post_reciever,sender = Post)
