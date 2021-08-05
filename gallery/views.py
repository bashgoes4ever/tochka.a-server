from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *


class Categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = GalleryCategory.objects.all()
        serializer = CategoriesSerializer(objs, many=True)
        return Response(serializer.data)


class GalleryImages(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category=None):
        if category:
            objs = GalleryCategory.objects.get(slug=category).images
        else:
            objs = GalleryImage.objects.all()
        serializer = GalleryImageSerializer(objs, many=True)
        return Response(serializer.data)


class Reviews(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Review.objects.all()
        serializer = ReviewSerializer(objs, many=True)
        return Response(serializer.data)