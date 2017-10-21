import requests
import datetime
from itertools import permutations
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


SKY_SCANNER_API_KEY = "ha696723343441434034465280137182"
HEADER = {'Accept': 'application/json'}
USER_COUNTRY = "HU"


class City(models.Model):
    name = models.CharField(max_length=255)
    api_code = models.CharField(max_length=100)

    @staticmethod
    def add(city_name):
        response = requests.get(get_city_code_request(city_name), headers=HEADER)
        data = response.json()
        for p in data['Places']:
            if city_name.lower() == p['PlaceName'].lower() and city_name[0].lower() == p['CityId'][0].lower():
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

    def get_route_to(self, other_city, interval_start, interval_end):
        min_price = None
        try:
            # Not flexible solution should use CityFrom.to_ts and CityTo.from_ts timestamps as interval
            response = requests.get(get_request(self.api_code, other_city.api_code, interval_start, interval_end),
                                    headers=HEADER)
            data = response.json()
            for q in data['Quotes']:
                if min_price is None or q['MinPrice'] < min_price:
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
    start_day = models.DateField(default=timezone.now)
    interval = models.DateField()

    def get_destinations(self):
        return Destination.objects.filter(trip=self)

    def get_cities(self):
        return [destination.city for destination in self.get_destinations()]

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
        return min([perm for perm in permutations(self.get_cities()) if
                    (perm[0].name == self.start_city.name and perm[len(perm) - 1].name == dest.name)], key=self.total_weight)

    def total_weight(self, cities):
        return sum([cities[i - 1].get_route_to(cities[i], self.start_day, self.interval) for i in range(1, len(cities))])

    @staticmethod
    def get_trips_of_user(user):
        return Trip.objects.filter(user=user)


class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    planned_days = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def get_fields(self):
        return {'city': self.city, 'days': self.planned_days}


def get_city_code_request(city_name, currency="EUR", locale="en-US"):
    return "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{country}/{currency}/{locale}?query={query}&apiKey={apiKey}".format(
        country=USER_COUNTRY,
        currency=currency,
        locale=locale,
        query=city_name,
        apiKey=SKY_SCANNER_API_KEY
    )


def get_request(origin_place, destination_place, outbound_partial_date, inbound_partial_date, currency="EUR", locale="en-US"):
    return "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}".format(
        country=USER_COUNTRY,
        currency=currency,
        locale=locale,
        originPlace=origin_place,
        destinationPlace=destination_place,
        outboundPartialDate=outbound_partial_date,
        inboundPartialDate=inbound_partial_date,
        apiKey=SKY_SCANNER_API_KEY
    )
