# coding=utf-8
from django.urls import path
from .views import *

urlpatterns = [
    path('tours/', Tours.as_view()),
    path('tour/<str:slug>/', SingleTour.as_view()),
]