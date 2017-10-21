from django.db import models
import datetime


class Trip(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField()
    start_day = models.DateField()

    def get_locations(self):
        return Location.objects.filter(trip=self)

    def get_duration(self):
        return sum(location.planned_days for location in self.get_locations())

    def get_last_day(self):
        return self.start_day + datetime.timedelta(days=self.get_duration())


class Location(models.Model):
    city_name = models.CharField(max_length=255)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
