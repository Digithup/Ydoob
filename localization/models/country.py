from cities.models import BaseCountry
from django.db import models


class CustomCountryModel(BaseCountry, models.Model):
    governorate = models.TextField()

    class Meta(BaseCountry.Meta):
        pass