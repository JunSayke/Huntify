from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', on_delete=models.CASCADE)


class Barangay(models.Model):
    name = models.CharField(max_length=100)
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE)
