from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'posts_count']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def get_posts_count(self, obj):
        return obj.posts.count()

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("邮箱地址不能为空")
        return value.lower()

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    slug = serializers.SlugField(required=False)
    tag_list = serializers.ListField(read_only=True)
    reading_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'summary', 
            'author', 'created_at', 'updated_at', 'published', 
            'featured_image', 'tags', 'tag_list', 'reading_time'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("标题长度不能少于5个字符")
        return value

    def validate_content(self, value):
        if len(value) < 100:
            raise serializers.ValidationError("文章内容不能少于100个字符")
        return value

    def validate_summary(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("摘要长度不能超过500个字符")
        return value

    def create(self, validated_data):
        # 如果没有提供摘要，自动生成
        if not validated_data.get('summary'):
            content = validated_data.get('content', '')
            validated_data['summary'] = content[:200] + '...' if len(content) > 200 else content
        return super().create(validated_data) 