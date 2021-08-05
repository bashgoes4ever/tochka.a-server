from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from rest_framework import status


class CreateOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.session.flush()
        return Response(status=status.HTTP_201_CREATED)