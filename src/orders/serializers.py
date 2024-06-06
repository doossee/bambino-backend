from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""

    class Meta:
        model = OrderItem
        fields = ("order", "product", "quantity")
        extra_kwargs = {"order": {"required": False}}

    def validate(self, attrs):
        if attrs["quantity"] > attrs["product"].balance:
            raise serializers.ValidationError("There is no so much products")


class OrderSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        order_items = []
        for item_data in items_data:
            product_data = item_data.pop("product")
            order_items.append(
                OrderItem(order=order, product=product_data, **item_data)
            )

        OrderItem.objects.bulk_create(order_items)
        return order
