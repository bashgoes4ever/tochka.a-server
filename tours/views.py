from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *


class Tours(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Tour.objects.all()
        serializer = TourCardSerializer(objs, many=True)
        return Response(serializer.data)


class SingleTour(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        obj = Tour.objects.get(slug=slug)
        serializer = SingleTourSerializer(obj, many=False)
        return Response(serializer.data)