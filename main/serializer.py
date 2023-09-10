from rest_framework import serializers

from main.serializers import ProductSerializer
from .models import *

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    products = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'