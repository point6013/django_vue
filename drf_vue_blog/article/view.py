from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django.http import JsonResponse
from article.models import Article
from article.serializers import ArticleListSerializer


@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serielizer = ArticleListSerializer(data=request.data)
        if serielizer.is_valid():
            serielizer.save()
            return Response(serielizer.data, status=status.HTTP_201_CREATED)
        return Response(serielizer.data, status=status.HTTP_400_BAD_REQUEST)
