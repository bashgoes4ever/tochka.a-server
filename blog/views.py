from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *


class Articles(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        if id:
            obj = Article.objects.get(id=id)
            serializer = ArticleSerializer(obj)
            return Response(serializer.data)
        else:
            if request.GET.get('tag'):
                objs = Article.objects.filter(tags__in=request.GET.get('tag'))
            else:
                objs = Article.objects.all()
            if request.GET.get('count'):
                objs = objs[:int(request.GET.get('count'))]
            serializer = ShortArticleSerializer(objs, many=True)
            return Response(serializer.data)


class Tags(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Tag.objects.all()
        serializer = TagsSerializer(objs, many=True)
        return Response(serializer.data)

