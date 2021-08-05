# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('shop/categories/<str:category>/', Categories.as_view()),
    path('shop/products/<str:category>/<str:subcategory>/', Products.as_view()),
    path('shop/products/<str:category>/', Products.as_view()),
    path('shop/filters/<str:category>/<str:subcategory>/', Filters.as_view()),
    path('shop/filters/<str:category>/', Filters.as_view()),
    path('shop/product/<str:slug>/', SingleProduct.as_view()),
]