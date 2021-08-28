from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        session_key = self.context['request'].session.session_key
        basket, created = Basket.objects.get_or_create(user=session_key)
        order, created = Order.objects.get_or_create(basket=basket, **validated_data)
        return order


class FormApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormApplication
        fields = '__all__'

    def create(self, validated_data):
        application, created = FormApplication.objects.get_or_create(**validated_data)
        return application
