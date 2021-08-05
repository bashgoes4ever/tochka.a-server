from rest_framework import serializers
from .models import *


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = '__all__'


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        exclude = ('category', 'priority',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('priority', 'image',)