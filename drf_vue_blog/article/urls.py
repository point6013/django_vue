from django.urls import path
from article import view

app_name = 'article'

urlpatterns = [
    path('', view.article_list, name='list')

]
