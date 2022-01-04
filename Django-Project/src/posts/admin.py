from django.contrib import admin

# Register your models here.
from .models import Post

#Built In Admin Function to Register the Post Model into Admin Site
admin.site.register(Post)