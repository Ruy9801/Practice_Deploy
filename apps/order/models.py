from django.db import models
from apps.customer.models import Customer
from apps.freelancer.models import Freelancer 


class OrderStatus(models.TextChoices):
    opened = 'opened'
    in_process = 'in_process'
    completed = 'completed'


class Order(models.Model):

    freelancer = models.ForeignKey(Freelancer, related_name='orders', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='descr_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.opened)

    def __str__(self) -> str:
        return f'id={self.id}.  [{self.customer} --> {self.freelancer}]'
    
    