from rest_framework import serializers
from .models import *


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImages
        fields = ('thumb', 'id', )


class ArticleSerializer(serializers.ModelSerializer):
    images = ArticleImageSerializer(many=True)

    class Meta:
        model = Article
        exclude = ('image', 'tags',)


class ShortArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('thumb', 'name', 'description', 'id',)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
