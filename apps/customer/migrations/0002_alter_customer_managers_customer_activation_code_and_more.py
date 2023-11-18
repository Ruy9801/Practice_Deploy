# Generated by Django 4.2.7 on 2023-11-18 09:03

import apps.customer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customer',
            managers=[
                ('objects', apps.customer.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='activation_code',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
