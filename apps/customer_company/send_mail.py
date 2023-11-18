from django.core.mail import send_mail 
from django.utils.html import format_html
from celery import shared_task
from time import sleep


@shared_task()
def send_confirmation_email(email, code):
    activation_url = f'http://localhost:8000/api/v1/cust_comp/activate/?u={code}'
    # sleep(6)
    send_mail(
        'Активируйте ваш аккаунт!',
        activation_url,
        'killer@gmail.com',
        [email],
        fail_silently=False,
    )
