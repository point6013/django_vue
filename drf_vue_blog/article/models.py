from django.db import models

# Create your models here.
from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from markdown import Markdown


class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """文章标签"""
    text = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Article(models.Model):
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)

    # 作者
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='articles')

    # tag
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')

    # 标题图
    avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_md(self):
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        md_body = md.convert(self.body)
        return md_body, md.toc
