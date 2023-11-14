# Generated by Django 4.2.7 on 2023-11-13 08:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='birth_date',
            field=models.DateField(default=datetime.date(1990, 1, 1)),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='price',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=10),
        ),
    ]
