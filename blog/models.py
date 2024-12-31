from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import re
import uuid
from pypinyin import lazy_pinyin

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    featured_image = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def generate_unique_slug(self, base_slug):
        """生成唯一的slug"""
        new_slug = base_slug
        counter = 1
        while Post.objects.filter(slug=new_slug).exclude(id=self.id).exists():
            new_slug = f"{base_slug}-{counter}"
            counter += 1
        return new_slug

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            # 检查标题是否包含中文字符
            if re.search(r'[\u4e00-\u9fff]', self.title):
                # 将中文转换为拼音
                pinyin_list = lazy_pinyin(self.title)
                # 将拼音列表组合成字符串，并移除非字母数字字符
                base_slug = re.sub(r'[^a-zA-Z0-9\s-]', '', ' '.join(pinyin_list))
                # 生成slug
                self.slug = self.generate_unique_slug(slugify(base_slug))
            else:
                # 英文标题直接使用slugify
                self.slug = self.generate_unique_slug(slugify(self.title))

            # 如果生成的slug为空（例如标题全是特殊字符），使用UUID
            if not self.slug:
                self.slug = str(uuid.uuid4())[:8]
        
        super().save(*args, **kwargs)
        