from django.db import models
from django.conf import settings
import datetime


class City(models.Model):
    name = models.CharField(max_length=255)


class Trip(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    completed = models.BooleanField()
    start_day = models.DateField()

    def get_destinations(self):
        return Destination.objects.filter(trip=self)

    def get_duration(self):
        return sum(destination.planned_days for destination in self.get_destinations())

    def get_last_day(self):
        return self.start_day + datetime.timedelta(days=self.get_duration())


class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
