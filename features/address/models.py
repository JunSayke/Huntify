from django.db import models


# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.title()


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey('Province', on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()


class Barangay(models.Model):
    name = models.CharField(max_length=100)
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()
