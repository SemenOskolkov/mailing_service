from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import *


app_name = BlogConfig.name

urlpatterns = [
    path('blog_list/', cache_page(120)(BlogListView.as_view()), name='blog_list'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),

    path('change_status_blog/<int:pk>/', change_status_blog, name='change_status_blog'),
]