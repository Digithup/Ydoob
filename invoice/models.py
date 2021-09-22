from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


from sales.models.orders import OrderProduct, Order
from vendors.models import Vendor

User = get_user_model()

# class Invoice(models.Model):
#     TERMS = [
#     ('14 days', '14 days'),
#     ('30 days', '30 days'),
#     ('60 days', '60 days'),
#     ]
#
#     STATUS = [
#     ('CURRENT', 'CURRENT'),
#     ('OVERDUE', 'OVERDUE'),
#     ('PAID', 'PAID'),
#     ]
#
#     title = models.CharField(null=True, blank=True, max_length=100)
#     number = models.CharField(null=True, blank=True, max_length=100)
#     dueDate = models.DateField(null=True, blank=True)
#     paymentTerms = models.CharField(choices=TERMS, default='14 days', max_length=100)
#     status = models.CharField(choices=STATUS, default='CURRENT', max_length=100)
#     notes = models.TextField(null=True, blank=True)
#
#     #RELATED fields
#     courier = models.ForeignKey(Courier, blank=True, null=True, on_delete=models.SET_NULL)
#     client = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
#     order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
#     order_product = models.ForeignKey(OrderProduct, blank=True, null=True, on_delete=models.SET_NULL)
#
#
#     #Utility fields
#     uniqueId = models.CharField(null=True, blank=True, max_length=100)
#     slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
#     date_created = models.DateTimeField(blank=True, null=True)
#     last_updated = models.DateTimeField(blank=True, null=True)
#
#
#     def __str__(self):
#         return '{} {}'.format(self.title, self.uniqueId)
#
#
#     def get_absolute_url(self):
#         return reverse('invoice-detail', kwargs={'slug': self.slug})
#
#     def save(self, *args, **kwargs):
#         if self.date_created is None:
#             self.date_created = timezone.localtime(timezone.now())
#         if self.uniqueId is None:
#             self.uniqueId = str(uuid4()).split('-')[4]
#             self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
#
#         self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
#         self.last_updated = timezone.localtime(timezone.now())
#
#         super(Invoice, self).save(*args, **kwargs)

class Invoice(models.Model):

    STATUS = [
    ('CURRENT', 'CURRENT'),
    ('OVERDUE', 'OVERDUE'),
    ('PAID', 'PAID'),
    ]

    title = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=100)
    dueDate = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default='CURRENT', max_length=100)
    notes = models.TextField(null=True, blank=True)

    #RELATED fields

    client = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.SET_NULL)

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    order_product = models.ForeignKey(OrderProduct, blank=True, null=True, on_delete=models.SET_NULL)


    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)


    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)


class Settings(models.Model):

    PROVINCES = [
    ('Gauteng', 'Gauteng'),
    ('Free State', 'Free State'),
    ('Limpopo', 'Limpopo'),
    ]

    #Basic Fields
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    order_product = models.ForeignKey(OrderProduct, blank=True, null=True, on_delete=models.SET_NULL)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{} {} {}'.format(self.order.email, self.order.address, self.uniqueId)


    def get_absolute_url(self):
        return reverse('settings-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.order.email, self.order.address, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.order.email, self.order.address, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Settings, self).save(*args, **kwargs)