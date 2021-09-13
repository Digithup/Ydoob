from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Governorates(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Governorates, self).save(*args, **kwargs)


class City(models.Model):
    governorates = models.ForeignKey(Governorates, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Area, self).save(*args, **kwargs)
