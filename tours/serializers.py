from rest_framework import serializers
from .models import *


class TourCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'short_name', 'short_description', 'card_thumb', 'slug',)


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = '__all__'


class TourStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourStep
        fields = '__all__'


class HowToFindSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourHowToFindImages
        fields = ('thumb',)


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourInterestingPlacesImages
        fields = ('thumb',)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourInventoryImages
        fields = ('thumb',)


class SingleTourSerializer(serializers.ModelSerializer):
    guides = GuideSerializer(many=True)
    faq_items = FAQSerializer(many=True)
    steps = TourStepSerializer(many=True)
    htfimgs = HowToFindSerializer(many=True)
    itimgs = PlaceSerializer(many=True)
    inventory_imgs = InventorySerializer(many=True)

    class Meta:
        model = Tour
        fields = '__all__'