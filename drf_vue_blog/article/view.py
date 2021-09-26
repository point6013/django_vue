from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from django.http import Http404
from rest_framework.views import APIView
from django.http import JsonResponse
from article.models import Article
from article.models import Category
from article.models import Tag
from article.models import Avatar
from rest_framework import viewsets
from article.serializers import ArticleSerializer, ArticleDetailSerializer
from article.serializers import CategorySerializer
from article.serializers import CategoryDetailSerializer
from article.serializers import TagSerializer
from article.serializers import AvatarSerializer
from django_filters.rest_framework import DjangoFilterBackend
# from article.serializers import ArticleListSerializer, ArticleDetailSerializer

from article.permission import IsAdminUserOrReadOnly
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


# 普通视图
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serielizer = ArticleListSerializer(data=request.data)
#         if serielizer.is_valid():
#             serielizer.save()
#             return Response(serielizer.data, status=status.HTTP_201_CREATED)
#         return Response(serielizer.data, status=status.HTTP_400_BAD_REQUEST)


# 列表的结构可以可以同样的修改

# class ArticleList(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUserOrReadOnly]
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer
#
#     # 这里面的serializer是serializer_class的实例，并且已经携带着验证后的数据
#     # save方法可以接受关键字参数作为额外的需要保存的数据
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# # 基于类的视图
#
# class ArticleDetail(APIView):
#     """文章详情视图"""
#
#     def get_object(self, pk):
#         """获取的那个对象"""
#         try:
#             return Article.objects.get(pk=pk)
#         except:
#             return Http404
#
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # drf 通用视图
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     """文章详情视图"""
#     permission_classes = [IsAdminUserOrReadOnly]
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer

# 代码重构

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

    permission_classes = [IsAdminUserOrReadOnly]
    # django_filters
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username', 'title']

    # 模糊搜索条件，rest_framework 的filter
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

    # serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
