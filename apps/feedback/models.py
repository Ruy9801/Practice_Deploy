from django.db import models
from apps.freelancer.models import Freelancer 
from apps.customer.models import Customer 
from apps.order.models import Order 


class FreelancerRating(models.Model):
    RATING_CHOICES = (
        (1, 'too bad'),
        (2, 'bad'),
        (3, 'normal'),
        (4, 'good'),
        (5, 'excellent')
    )

    freelancer = models.ForeignKey(Freelancer, related_name='ratings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ['freelancer', 'customer']



class Favorite(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='favorites')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorite_freelancers')

    class Meta:
        unique_together = ['freelancer', 'customer']