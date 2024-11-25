# models.py
from django.db import models


class Rating(models.Model):
    user = models.ForeignKey('authentication.User', related_name="ratings", on_delete=models.CASCADE)
    boarding_room = models.ForeignKey('property_management.BoardingRoom', related_name="ratings",
                                      on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    feedback = models.TextField(max_length=2000)  # New feedback field

    def __str__(self):
        return f"{self.user} - {self.boarding_room} - {self.rating}"
