from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime
from .models import Post
from .serializers import PostSerializer, UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'summary', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Post.objects.all()
        
        # 非管理员只能看到已发布的文章
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)

        # 获取查询参数
        search = self.request.query_params.get('search', None)
        tags = self.request.query_params.get('tags', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        # 搜索标题和内容
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(summary__icontains=search)
            )

        # 按标签筛选
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            tag_query = Q()
            for tag in tag_list:
                tag_query |= Q(tags__icontains=tag)
            queryset = queryset.filter(tag_query)

        # 按日期范围筛选
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=start)
            except ValueError:
                pass

        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(created_at__lte=end)
            except ValueError:
                pass

        return queryset.distinct()

    def perform_create(self, serializer):
        if not serializer.validated_data.get('slug'):
            title = serializer.validated_data.get('title', '')
            base_slug = slugify(title)
            
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            serializer.validated_data['slug'] = slug
        
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if 'title' in serializer.validated_data and not serializer.validated_data.get('slug'):
            title = serializer.validated_data.get('title')
            base_slug = slugify(title)
            
            slug = base_slug
            counter = 1
            while Post.objects.exclude(pk=serializer.instance.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            serializer.validated_data['slug'] = slug
        
        serializer.save()

    @action(detail=False, methods=['get'])
    def published(self, request):
        posts = self.get_queryset().filter(published=True)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def drafts(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized"}, status=403)
        posts = self.get_queryset().filter(published=False)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tags(self, request):
        """获取所有标签列表"""
        tags = set()
        for post in Post.objects.filter(published=True):
            if post.tags:
                tags.update([tag.strip() for tag in post.tags.split(',')])
        return Response(sorted(list(tags)))

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                      status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'},
                      status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    
    return Response({
        'token': token.key,
        'user': serializer.data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.user.auth_token:
        request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)