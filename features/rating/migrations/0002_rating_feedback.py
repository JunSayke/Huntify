# Generated by Django 5.1.3 on 2024-11-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='feedback',
            field=models.TextField(default='Testing', max_length=2000),
            preserve_default=False,
        ),
    ]
