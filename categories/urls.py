# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', Categories.as_view()),
]