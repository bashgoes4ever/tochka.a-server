from rest_framework import serializers
from .models import *
from products.serializers import CategoriesSerializer


class CategorySerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True)

    class Meta:
        model = CategoryCard
        fields = '__all__'