# Generated by Django 5.1.3 on 2024-11-24 10:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_management', '0004_boardingroomtenant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardingroomtenant',
            name='boarding_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_tenants', to='property_management.boardingroom'),
        ),
        migrations.AlterField(
            model_name='boardingroomtenant',
            name='check_in_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='boardingroomtenant',
            name='check_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='boardingroomtenant',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boarding_rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
