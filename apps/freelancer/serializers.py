from rest_framework import serializers 
from django.contrib.auth import get_user_model 


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = User 
        fields = ('balance', 'birth_date','what_i_can', 'price', 'work_time', 'city', 'email', 'password', 'password_confirm', 'last_name', 'first_name', 'avatar', 'phone_number')
        ref_name = 'FreelancerUserSerializer'

    def validate(self, attrs):
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
        user = User.objects.create_user(**validated_data)
        return user
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        exclude = ('password', )
        ref_name = 'FreelancerUserSerializer'
        

