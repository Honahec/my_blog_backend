from django.db import models
from django.contrib.auth.models import User
from .utils import SlugGenerator, TagManager

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(unique=True, max_length=255, blank=True, verbose_name='URL别名')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(blank=True, verbose_name='摘要')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='作者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published = models.BooleanField(default=False, verbose_name='是否发布')
    featured_image = models.URLField(blank=True, verbose_name='特色图片')
    tags = models.CharField(max_length=200, blank=True, verbose_name='标签')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 生成slug
        if not self.slug and self.title:
            self.slug = SlugGenerator.generate_unique_slug(
                self.title,
                Post,
                self.id
            )
        
        # 标准化标签
        if self.tags:
            self.tags = TagManager.normalize_tags(self.tags)
            
        super().save(*args, **kwargs)

    @property
    def tag_list(self):
        """返回标签列表"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    @property
    def reading_time(self):
        """估算阅读时间（分钟）"""
        words_per_minute = 200  # 假设平均阅读速度
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))
        