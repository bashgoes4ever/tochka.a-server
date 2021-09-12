from rest_framework import serializers
from .models import *


class PageMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMeta
        exclude = ('url', 'id',)
