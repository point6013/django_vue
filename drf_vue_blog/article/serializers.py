from rest_framework import serializers
from article.models import Article


# class ArticleListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True, max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()


#
# ModelSerializer 的功能与上一章的 Serializer 基本一致，不同的是它额外做了些工作：
#
# 自动推断需要序列化的字段及类型
# 提供对字段数据的验证器的默认实现
# 提供了修改数据需要用到的 .create() 、 .update() 方法的默认实现

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['id',
        #           'title',
        #           'created']
        fields = "__all__"
