from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .models import Shop, Product
from .serializers import (
    ShopSerializer,
    ShopDetailSerializer,
    SuppliesCreateSerializer,
    SalesSerializer,
    ProductCreateSerializer
)


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ShopDetailSerializer(instance)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='supply')
    def supply(self, request, *args, **kwargs):
        if type(request.data) == list:
            for item in request.data:
                item['shop'] = int(kwargs['pk'])
        else:
            request.data['shop'] = int(kwargs['pk'])
        serializer = SuppliesCreateSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)

    @action(methods=['POST'], detail=True, url_path='buy')
    def buy(self, request, *args, **kwargs):
        if type(request.data) == list:
            for item in request.data:
                item['shop'] = int(kwargs['pk'])
        else:
            request.data['shop'] = int(kwargs['pk'])
        serializer = SalesSerializer(data=request.data, many=isinstance(request.data, list))

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product
