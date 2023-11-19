from rest_framework import serializers 
from .models import Order 


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order 
        fields = ('freelancer', 'customer', 'company_name', 'created_at', 'finished_at', 'images', 'price', 'description')

