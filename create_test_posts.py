import os
import django
from django.utils.text import slugify

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog_backend.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

def create_test_posts():
    # 创建管理员用户
    admin_user, created = User.objects.get_or_create(
        username='admin',
        email='admin@example.com'
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True  # 设置为管理员
        admin_user.is_superuser = True  # 设置为超级用户
        admin_user.save()
    
    # 测试文章数据
    posts_data = [
        {
            'title': '现代化博客开发实践',
            'slug': 'modern-blog-development',
            'content': '在这篇文章中，我们将探讨如何使用 Vue.js 和 Django 构建现代化的博客系统...',
            'summary': '探索使用 Vue.js 和 Django 构建博客系统的最佳实践',
            'published': True,
            'tags': ['Vue.js', 'Django', 'Web Development']
        },
        {
            'title': 'RESTful API 最佳实践',
            'slug': 'restful-api-best-practices',
            'content': 'RESTful API 设计的核心原则和最佳实践，包括认证、版本控制、错误处理等...',
            'summary': '深入理解 RESTful API 设计原则和实践指南',
            'published': True,
            'tags': ['API', 'REST', 'Backend']
        },
        {
            'title': 'Python 异步编程指南',
            'slug': 'python-async-programming-guide',
            'content': '详细介绍 Python 中的异步编程概念，包括 async/await、协程等...',
            'summary': '学习 Python 异步编程的基础知识和进阶技巧',
            'published': True,
            'tags': ['Python', 'Async', 'Programming']
        }
    ]

    # 创建文章
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'content': post_data['content'],
                'summary': post_data['summary'],
                'published': post_data['published'],
                'author': admin_user,
                'tags': post_data['tags']
            }
        )
        if created:
            print(f"Created post: {post.title}")

if __name__ == '__main__':
    create_test_posts() 