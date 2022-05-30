from django import forms
from django.forms import SelectDateWidget, fields
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish =forms.DateField(widget=forms.SelectDateWidget) #--Making publish to a date picker
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
            ]