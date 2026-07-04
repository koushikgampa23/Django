from django.shortcuts import render
from rest_framework.decorators import api_view
from advanced_concepts.models import Product, Order
from advanced_concepts.serializers import ProductSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from advanced_concepts.filters import ProductFilter, InStockProductFilter
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def valid_products(self, request):
        products = self.get_queryset().filter(stock__gt=2)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)
