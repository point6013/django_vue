from django.db import models

# Create your models here.
from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User


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
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='article')

    def __str__(self):
        return self.title
