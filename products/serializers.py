from rest_framework import serializers
from .models import *


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('product', 'id', 'image')


class ProductCardSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = ('images', 'name', 'slug', 'price', 'id', 'old_price', 'hour_rate')


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        exclude = ('id', )


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(many=False)

    class Meta:
        model = ProductCharacteristic
        exclude = ('product', )


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True)
    category = CategoriesSerializer(many=False)
    characteristics = ProductCharacteristicSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('tags',)
