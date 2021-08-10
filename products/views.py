from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from django.core.paginator import Paginator


class Categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category):
        objs = ProductCategory.objects.filter(base_category=category)
        serializer = CategoriesSerializer(objs, many=True)
        return Response(serializer.data)


class Products(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category, subcategory=None):
        filters = {
            'category__base_category': category
        }

        if subcategory:
            filters['category__slug'] = subcategory

        if len(request.GET.getlist('filters')) > 0:
            filters['tags__in'] = request.GET.getlist('filters')

        objs = Product.objects.filter(**filters)

        filters = ProductTag.objects.filter(products__in=objs)
        filter_serializer = ProductTagSerializer(filters, many=True)

        paginator = Paginator(objs, 9)
        page_num = request.GET.get('page', 1)
        paginated_objs = paginator.get_page(page_num)

        serializer = ProductCardSerializer(paginated_objs, many=True)
        return Response({
            'data': serializer.data,
            'total_pages': paginator.num_pages,
        })


class SingleProduct(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        obj = Product.objects.get(slug=slug)
        serializer = ProductSerializer(obj, many=False)
        return Response(data=serializer.data)


class Filters(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category, subcategory=None):
        if subcategory:
            objs = Product.objects.filter(category__base_category=category, category__slug=subcategory)
        else:
            objs = Product.objects.filter(category__base_category=category)

        filters = ProductTag.objects.filter(products__in=objs).distinct()
        filter_serializer = ProductTagSerializer(filters, many=True)
        return Response(filter_serializer.data)