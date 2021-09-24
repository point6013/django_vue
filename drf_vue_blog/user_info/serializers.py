from django.contrib.auth.models import User
from rest_framework import serializers


class UserDescSerializer(serializers.ModelSerializer):
    """用于文章列表中引用的套嵌序列化器"""

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined'
        ]
