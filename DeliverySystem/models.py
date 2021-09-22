from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Create your models here.
from localization.models.models import Country, Governorates
from sales.models.orders import Order
from user.models import UserAddress
from vendors.models import Vendor

User = get_user_model()

class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    governorates = models.ForeignKey(Governorates, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.governorates

class Courier(models.Model):
    STATUS = (
        ('True', 'Yes'),
        ('False', 'NO'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    based_on_district = models.ManyToManyField(
        Location, related_name="delivery_district", blank=True)
    paypal_email = models.EmailField(max_length=255, blank=True)
    fcm_token = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.user.first_name


class Shipping(models.Model):
    CREATING_STATUS = 'creating'
    PROCESSING_STATUS = 'processing'
    PICKING_STATUS = 'picking'
    DELIVERING_STATUS = 'delivering'
    COMPLETED_STATUS = 'completed'
    CANCELED_STATUS = 'canceled'
    STATUSES = (
        (CREATING_STATUS, 'Creating'),
        (PROCESSING_STATUS, 'Processing'),
        (PICKING_STATUS, 'Picking'),
        (DELIVERING_STATUS, 'Delivering'),
        (COMPLETED_STATUS, 'Completed'),
        (CANCELED_STATUS, 'Canceled'),
    )

    # Step 1
    courier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    # Step 2
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    vendor_lat = models.FloatField(default=0)
    vendor_lng = models.FloatField(default=0)

    # Step 3
    customer = models.ForeignKey(UserAddress, on_delete=models.CASCADE, null=True, blank=True)
    customer_lat = models.FloatField(default=0)
    customer_lng = models.FloatField(default=0)

    # Step 4
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    # Extra info
    pickup_photo = models.ImageField(upload_to='job/pickup_photos/', null=True, blank=True)
    pickup_at = models.DateTimeField(null=True, blank=True)

    delivery_photo = models.ImageField(upload_to='job/delivery_photos/', null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.order


class Transaction(models.Model):
    IN_STATUS = "in"
    OUT_STATUS = "out"
    STATUSES = (
        (IN_STATUS, 'In'),
        (OUT_STATUS, 'Out'),
    )

    code=models.CharField(max_length=255,blank=True,null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE,default='1')
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default=IN_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code
