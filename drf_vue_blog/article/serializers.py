from rest_framework import serializers
from article.models import Article, Category, Tag, Avatar
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer


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


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    """博文序列化器"""
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    # category
    category = CategorySerializer(read_only=True)
    # category id
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # categoy id 字段的验证器
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, required=False, slug_field='text')

    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    def validate_avatar_id(self, value):
        if not Avatar.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError('Avatar with id {} not exists'.format(value))
        return value

    # 'C:\Users\Fred-Huang\Pictures\background.jpg'
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exist() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists".format(value))
        return value


class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {'body': {'write_only': True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


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


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""

    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError("Tag with text{} exists".format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = "__all__"
