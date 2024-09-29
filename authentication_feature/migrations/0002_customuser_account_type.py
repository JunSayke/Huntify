# Generated by Django 5.1.1 on 2024-09-29 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_feature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_type',
            field=models.CharField(choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')], default='tenant', max_length=10),
        ),
    ]
