from django.db import models
from apps.customer.models import Customer
from apps.freelancer.models import Freelancer 
from apps.customer_company.models import CustomerCompany


class Order(models.Model):

    freelancer = models.ForeignKey(Freelancer, related_name='orders', on_delete=models.CASCADE)

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.ForeignKey(CustomerCompany, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='descr_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.customer} or {self.company_name} -> {self.freelancer}'
    
    