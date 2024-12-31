from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'summary', 'author',
                 'created_at', 'updated_at', 'published', 'featured_image', 'tags']
        read_only_fields = ['created_at', 'updated_at'] 