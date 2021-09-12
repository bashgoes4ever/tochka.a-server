from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import *


class PageMetaView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        url = request.GET.get('url')
        if not url:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = PageMeta.objects.get(url=url)
        serializer = PageMetaSerializer(obj, many=False)
        return Response(serializer.data)