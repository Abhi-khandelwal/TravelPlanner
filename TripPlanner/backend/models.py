# IMPORTS
import requests
import datetime
from itertools import permutations
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# CONSTANTS
SKY_SCANNER_API_KEY = "ha696723343441434034465280137182"
HEADER = {'Accept': 'application/json'}
USER_COUNTRY = "HU"


class City(models.Model):
    name = models.CharField(max_length=255)
    api_code = models.CharField(max_length=100)

    @staticmethod
    def add(city_name):
        response = requests.get(getCityCodeRequest(city_name), headers=HEADER)
        data = response.json()
        for p in data['Places']:
            if (city_name.lower() == p['PlaceName'].lower() and city_name[0].lower() == p['CityId'][0].lower()):
                city = City(name=city_name, api_code=p['CityId'][:4])
                city.save()
                return city

        return None

    @staticmethod
    def get_or_add(city_name):
        try:
            return City.objects.get(name=city_name)
        except ObjectDoesNotExist:
            return City.add(city_name)

    def get_route_to(self, other_city):
        min_price = None
        try:
            # Not flexible solution should use CityFrom.to_ts and CityTo.from_ts timestamps as interval
            response = requests.get(getRequest(self.api_code, other_city.api_code, CityFrom.from_ts, CityFrom.to_ts),
                                    headers=HEADER)
            data = response.json()
            for q in data['Quotes']:
                if (min_price == None or q['MinPrice'] < min_price):
                    min_price = q['MinPrice']
        except Exception as exc:
            print(str(exc))
        print(self.name + ' -> ' + other_city.name + ': ' + str(min_price))
        return min_price

    def get_hotels(self):
        # api keres, parameter: self.api_code
        return None


class Trip(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    completed = models.BooleanField(default=False)
    start_city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    start_day = models.DateField(default=timezone.now())
    interval = models.DateField()

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

    def traveling_salesman(self, dest):
        return min([perm for perm in permutations([destination.city for destination in self.get_destinations()]) if
                    (perm[0].name == self.start_city.name and perm[len(perm) - 1].name == dest.name)], key=total_weight)

    def total_weight(self):
        total_weight(self.traveling_salesman())

    @staticmethod
    def get_trips_of_user(user):
        return Trip.objects.filter(user=user)


class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def get_fields(self):
        return {'city': self.city, 'days': self.planned_days}





def getCityCodeRequest(city_name, currency="EUR", locale="en-US"):
    return """http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{country}/{currency}/{locale}?query={query}&apiKey={apiKey}""".format(
        country=USER_COUNTRY,
        currency=currency,
        locale=locale,
        query=city_name,
        apiKey=SKY_SCANNER_API_KEY
    )


def getRequest(originPlace, destinationPlace, outboundPartialDate, inboundPartialDate, currency="EUR", locale="en-US"):
    return """http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}""".format(
        country=USER_COUNTRY,
        currency=currency,
        locale=locale,
        originPlace=originPlace,
        destinationPlace=destinationPlace,
        outboundPartialDate=outboundPartialDate,
        inboundPartialDate=inboundPartialDate,
        apiKey=SKY_SCANNER_API_KEY
    )


def total_weight(cities):
    return sum([cities[i - 1].get_route_to(cities[i]) for i in range(1, len(cities))])
