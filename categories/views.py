from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *


class Categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = CategoryCard.objects.all()
        serializer = CategorySerializer(objs, many=True)
        return Response(serializer.data)