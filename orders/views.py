from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from rest_framework import status
import requests


class CreateOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'created'
        }
        if serializer.data['payment_type'] is 'bank_card':
            user_name = 'T262800685953-api'
            password = 'T262800685953'
            order_number = serializer.data['id']
            amount = serializer.data['total_price']*100
            url = 'https://3dsec.sberbank.ru/payment/rest/register.do?userName={}&password={}&orderNumber={}&returnUrl=https://tochka-a-sochi.ru&amount={}'.format(
                user_name, password, order_number, amount)
            r = requests.get(url)
            response['payment_data'] = r.json()
        request.session.flush()
        return Response(data=response, status=status.HTTP_201_CREATED)


class CreateApplicationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FormApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
