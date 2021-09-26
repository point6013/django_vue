from rest_framework import serializers
from article.models import Article, Category
from user_info.serializers import UserDescSerializer


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
#
# class ArticleListSerializer(serializers.ModelSerializer):
#     author = UserDescSerializer(read_only=True)
#     url = serializers.HyperlinkedIdentityField(view_name='article:detail')
#
#     class Meta:
#         model = Article
#         fields = [
#             # 'id',
#             'url',
#             'title',
#             'body',
#             'created',
#             # 'updated',
#             'author',
#         ]
#         # fields = "__all__"
#
#
# class ArticleDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'


# 代码重构， 视图级序列化简化之前的代码
class CategorySerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['created']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """博文序列化器"""
    author = UserDescSerializer(read_only=True)
    # category
    category = CategorySerializer(read_only=True)
    # category id
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # categoy id 字段的验证器

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exist() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists".format(value))
        return value

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = ['url', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'created', 'articles']
