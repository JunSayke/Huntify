# Generated by Django 5.1.1 on 2024-11-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_feature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
    ]
