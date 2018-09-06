from django.db import models
from django.utils import timezone

# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length = 30)
    country = models.CharField(max_length = 10)
    temp = models.FloatField(blank = True, null=True)
    desc = models.CharField(max_length = 40, blank = True, null=True)
    time = models.DateTimeField(blank = True)
    icon = models.CharField(max_length = 15, blank = True, null=True)

    def __str__(self):
        return self.city
