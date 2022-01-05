from django.contrib import admin
from .models import Post
# Register your models here.

#--- Model Admin Decides how we can display the Colums and helps us customize them in
#--- Admin Page of Your Application
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated","timestamp"] #-- Chooses which colums to display
    # list_display_links = ["updated"] #-- To Change the Link to The Content
    list_filter = ["updated","timestamp"] #-- To Give Filter Options
    search_fields = ["title","content"] #-- Includes a Search field for mentioned Fields
    class Meta:
        model = Post

admin.site.register(Post,PostModelAdmin)
