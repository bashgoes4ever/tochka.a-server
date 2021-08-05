from rest_framework import serializers
from .models import *
from products.serializers import ProductCardSerializer


class ProductInBasketSerializer(serializers.ModelSerializer):
    product = ProductCardSerializer()

    class Meta:
        model = ProductInBasket
        exclude = ('basket',)


class ProductInBasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInBasket
        fields = '__all__'

    def create(self, validated_data):
        product, created = ProductInBasket.objects.get_or_create(**validated_data)
        return product


class ProductInBasketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInBasket
        exclude = ('product', 'basket',)

    def update(self, instance, validated_data):
        instance.quantity = int(validated_data.get("quantity", instance.quantity))
        instance.save()
        return instance


class BasketSerializer(serializers.ModelSerializer):
    products = ProductInBasketSerializer(many=True)

    class Meta:
        model = Basket
        exclude = ('user',)
