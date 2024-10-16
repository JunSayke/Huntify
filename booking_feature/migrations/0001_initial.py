# Generated by Django 5.1 on 2024-10-16 12:56

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardingHouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='boarding house id')),
                ('name', models.CharField(max_length=100, verbose_name='boarding house name')),
                ('description', models.TextField(verbose_name='description')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoardingHouseImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='image id')),
                ('image', models.FileField(upload_to='boarding_house_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('boarding_house_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='booking_feature.boardinghouse')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='room id')),
                ('name', models.CharField(max_length=100, verbose_name='room name')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('is_available', models.BooleanField(default=True, verbose_name='is available')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('boarding_house_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='booking_feature.boardinghouse')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='booking id')),
                ('booking_schedule', models.DateTimeField(verbose_name='schedule')),
                ('booking_status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=10, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking_feature.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='image id')),
                ('image', models.FileField(upload_to='room_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='booking_feature.room')),
            ],
        ),
    ]
