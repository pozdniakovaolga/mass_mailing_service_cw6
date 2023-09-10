from django.urls import path
from blog.views import ArticleListView, ArticleDetailView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('list/', ArticleListView.as_view(), name='article_list'),
    path('article_view/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]