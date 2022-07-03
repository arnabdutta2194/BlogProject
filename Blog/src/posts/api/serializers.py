from pyexpat import model
from rest_framework import serializers

from posts.models import Post


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','publish']


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','slug','content','publish','read_time']


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','slug','content','publish','read_time']
        