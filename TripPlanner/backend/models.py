from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import datetime


class City(models.Model):
    name = models.CharField(max_length=255)
    api_code = models.CharField(max_length=100)

    @staticmethod
    def add(city_name):
        # api keres a city name-re
        if True: # ha van ra talalat
            api_code = 'code_here'
            city = City(name=city_name, api_code=api_code)
            city.save()
            return city
        else:
            return None

    @staticmethod
    def get_or_add(city_name):
        try:
            return City.objects.get(name=city_name)
        except ObjectDoesNotExist:
            return City.add(city_name)

    def get_route_to(self, other_city):
        # api keres, parameterek: self.api_code, other_city.api_code
        return None

    def get_hotels(self):
        # api keres, parameter: self.api_code
        return None


class Trip(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    completed = models.BooleanField(default=False)
    start_day = models.DateField()

    def get_destinations(self):
        return Destination.objects.filter(trip=self)

    def get_duration(self):
        return sum(destination.planned_days for destination in self.get_destinations())

    def get_last_day(self):
        return self.start_day + datetime.timedelta(days=self.get_duration())

    def get_data(self):
        return {
            'name': self.name,
            'destinations': [destination.get_fields() for destination in self.get_destinations()]
        }

    @staticmethod
    def get_trips_of_user(user):
        return Trip.objects.filter(user=user)


class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def get_fields(self):
        return {'city': self.city, 'days': self.planned_days}
