from django.urls import path
from article import view

app_name = 'article'

urlpatterns = [
    path('', view.article_list, name='list'),
    path('<int:pk>/', view.ArticleDetail.as_view(), name='detail'),
]
