from datetime import datetime, date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from rest_framework import status
from orders.models import get_product_units_for_date_range


class BasketView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            # if 'HTTP_AUTHORIZATION' not in request.META:
            #     request.session.create()
            #     session_key = request.session.session_key
            # else:
            #     session_key = request.META['HTTP_AUTHORIZATION']
            if not request.session.exists(request.session.session_key):
                request.session.create()
            session_key = request.session.session_key
            obj, created = Basket.objects.get_or_create(user=session_key)
            serializer = BasketSerializer(obj)
            return Response(data=serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductInBasketView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, product_id):
        try:
            basket, created = Basket.objects.get_or_create(user=request.session.session_key)
            product = Product.objects.get(id=product_id)
            serializer = ProductInBasketCreateSerializer(data={
                "basket": basket.id,
                "product": product_id,
                "quantity": 1
            })

            check_hour_rate(basket, product.hour_rate)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            basket_serializer = BasketSerializer(basket)

            return Response(data=basket_serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = ProductInBasket.objects.get(id=product_id)
            serializer = ProductInBasketUpdateSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(product, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            product = ProductInBasket.objects.get(id=product_id)
            product.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Range:
    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to


class CheckAvailability(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        basket, created = Basket.objects.get_or_create(user=request.session.session_key)
        res = []
        if len(basket.products.all()) > 0:
            date_from = datetime.fromtimestamp(request.data['from']/1000)
            date_to = datetime.fromtimestamp(request.data['to']/1000)
            range = Range(datetime(year=date_from.year, month=date_from.month, day=date_from.day, hour=date_from.hour), datetime(year=date_to.year, month=date_to.month, day=date_to.day, hour=date_to.hour))

            for product_in_basket in basket.products.all():
                # найти product_units, которые можно забронировать на выбранные даты
                product_units = get_product_units_for_date_range(product_in_basket, range, False)

                # если найденное количество товаров меньше необходимого, выдаем ошибку
                if len(product_units) < product_in_basket.quantity:
                    product = ProductInBasket.objects.get(id=product_in_basket.id)
                    product.quantity = len(product_units)
                    product.save()
                    res.append({
                        'id': product_in_basket.id,
                        'max_value': len(product_units),
                        'error': True
                    })
                else:
                    res.append({
                        'id': product_in_basket.id,
                        'max_value': len(product_units),
                        'error': False
                    })

        return Response({
            'data': res,
            'status': status.HTTP_200_OK
        })


def check_hour_rate(basket, hour_rate):
    same = True
    for p in basket.products.all():
        if p.product.hour_rate is not hour_rate:
            same = False
            break
    if not same:
        for product in basket.products.all():
            product.delete()
