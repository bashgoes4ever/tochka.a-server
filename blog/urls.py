# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('blog/articles/<int:id>', Articles.as_view()),
    path('blog/articles/', Articles.as_view()),
    path('blog/tags/', Tags.as_view()),
]