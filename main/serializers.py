from rest_framework import serializers
from .models import *

class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__' 

class ProductSerializer(serializers.ModelSerializer):
    quantity_type = QuantitySerializer()
    class Meta:
        model = Product
        fields = '__all__'