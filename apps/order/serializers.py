from rest_framework import serializers 
from apps.order.models import Order 
from apps.freelancer.models import Freelancer 
from apps.customer.models import Customer


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), default=None)
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all())
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order 
        fields = '__all__'