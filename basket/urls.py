# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('basket/', BasketView.as_view()),
    path('basket/product/<int:product_id>', ProductInBasketView.as_view()),
    path('basket/check/', CheckAvailability.as_view()),
]