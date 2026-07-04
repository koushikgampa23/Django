from rest_framework import serializers
from advanced_concepts.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "description"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        for product in products_data:
            product = Product.objects.create(**product)
            order.products.add(product)
        return order

    class Meta:
        model = Order
        fields = "__all__"

    #     extra_kwargs = {"user": {"read_only": True}}
