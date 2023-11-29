from rest_framework import serializers 
from apps.freelancer.models import Freelancer
from django.db.models import Avg
from apps.order.serializers import Order, OrderSerializer



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = Freelancer 
        fields = ('balance', 'company_name', 'birth_date','what_i_can', 'price', 'work_time', 'city', 'email', 'password', 'password_confirm', 'last_name', 'first_name', 'avatar', 'phone_number')
        ref_name = 'FreelancerUserSerializer'

    
    def validate(self, attrs):
        phone_number = attrs['phone_number'].strip()
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise  serializers.ValidationError(
                'Passwords didnt match!'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password feild must contain alpha and numeric symbols'
            )
        return attrs
    
    def create(self, validated_data):
        user = Freelancer.objects.create_user(**validated_data)
        return user
    
    
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer 
        exclude = ('password', )
        ref_name = 'FreelancerUserSerializer'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        rating_info = instance.ratings.aggregate(Avg('rating'))
        average_rating = rating_info.get('rating__avg', None)
        rating_count = instance.ratings.count()
        repr['rating'] = {
            'average_rating': average_rating,
            'rating_count': rating_count,
        }
        orders = Order.objects.filter(freelancer=instance)
        order_data = OrderSerializer(instance=orders, many=True).data
        repr['history'] = order_data

        return repr
        

