# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('gallery/categories/', Categories.as_view()),
    path('gallery/images/<str:category>/', GalleryImages.as_view()),
    path('gallery/images/', GalleryImages.as_view()),
    path('reviews/', Reviews.as_view()),
]