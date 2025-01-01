from django.utils.text import slugify
from pypinyin import lazy_pinyin
import re
import uuid

class SlugGenerator:
    @staticmethod
    def generate_unique_slug(title, model_class, instance_id=None):
        """
        生成唯一的slug
        :param title: 标题
        :param model_class: 模型类
        :param instance_id: 当前实例ID（用于更新时排除自身）
        :return: 唯一的slug
        """
        if re.search(r'[\u4e00-\u9fff]', title):
            # 将中文转换为拼音
            pinyin_list = lazy_pinyin(title)
            # 将拼音列表组合成字符串，并移除非字母数字字符
            base_slug = re.sub(r'[^a-zA-Z0-9\s-]', '', ' '.join(pinyin_list))
            base_slug = slugify(base_slug)
        else:
            # 英文标题直接使用slugify
            base_slug = slugify(title)

        # 如果生成的slug为空，使用UUID
        if not base_slug:
            return str(uuid.uuid4())[:8]

        # 确保slug唯一
        slug = base_slug
        counter = 1
        query = model_class.objects.filter(slug=slug)
        if instance_id:
            query = query.exclude(id=instance_id)
        
        while query.exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            query = model_class.objects.filter(slug=slug)
            if instance_id:
                query = query.exclude(id=instance_id)

        return slug

class TagManager:
    @staticmethod
    def normalize_tags(tags_str):
        """
        标准化标签字符串
        :param tags_str: 原始标签字符串
        :return: 标准化后的标签字符串
        """
        if not tags_str:
            return ""
        
        # 分割标签，去除空白，去重，排序
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        tags = sorted(set(tags))
        
        return ','.join(tags)

    @staticmethod
    def get_all_tags(queryset):
        """
        从查询集中获取所有唯一标签
        :param queryset: 文章查询集
        :return: 排序后的标签列表
        """
        tags = set()
        for obj in queryset:
            if obj.tags:
                tags.update(tag.strip() for tag in obj.tags.split(','))
        return sorted(list(tags)) 