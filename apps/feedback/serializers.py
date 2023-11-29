from rest_framework import serializers
from .models import FreelancerRating, Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'freelancer', 'customer']

class FreelancerRatingSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')
    freelancer = serializers.ReadOnlyField(source='freelancer.id')

    class Meta:
        model = FreelancerRating
        fields = '__all__'

