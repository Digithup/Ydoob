from catalog.models.models import STATUS, Products
from django.db import models
# Create your models here.



class FiltersGroup(models.Model):
    title = models.CharField(max_length=100, unique=True )
    sort_order = models.IntegerField( default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Filters(models.Model):
    title = models.CharField(max_length=100, unique=True)
    filter_group = models.ForeignKey(FiltersGroup, on_delete=models.CASCADE ,null=True)
    sort_order = models.IntegerField(default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class AttributesGroup(models.Model):
    title = models.CharField(max_length=100,  )
    sort_order = models.IntegerField(default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Attributes(models.Model):
    title = models.CharField(max_length=100,unique=True )
    attributes_group = models.ForeignKey(AttributesGroup, on_delete=models.CASCADE , null=True)
    sort_order = models.IntegerField(default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class OptionsType(models.Model):
    title = models.CharField(max_length=100,unique=True )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Options(models.Model):
    title = models.CharField(max_length=100,unique=True )

    sort_order = models.IntegerField(default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Manufacturer(models.Model):
    title = models.CharField(max_length=100,  unique=True)
    image = models.ImageField(upload_to='images/Manufacturer/%Y/', null=True, default='images/Manufacturer/en-gb.png')
    sort_order = models.IntegerField(default=0)
    slug = models.SlugField(null=title, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


