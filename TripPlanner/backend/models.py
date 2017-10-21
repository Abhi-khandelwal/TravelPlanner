from django.db import models


class Location(models.Model):
    city_name = models.CharField(max_length=255)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Trip(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField()
    start_day = models.DateField()
