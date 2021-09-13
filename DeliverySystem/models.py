import uuid

from django.contrib.auth import get_user_model
from django.db import models

from django.utils import timezone

# Create your models here.
from sales.models.orders import Order

User = get_user_model()

class Location(models.Model):
    province = models.CharField(
        max_length=254, null=False, blank=False, default="Province 3")
    district = models.CharField(
        max_length=254, null=False, blank=False, default="Qena")

    def __str__(self):
        return self.district

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


class Category(models.Model):
    slug = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Job(models.Model):
    SMALL_SIZE = "small"
    MEDIUM_SIZE = "medium"
    LARGE_SIZE = "large"
    SIZES = (
        (SMALL_SIZE, 'Small'),
        (MEDIUM_SIZE, 'Medium'),
        (LARGE_SIZE, 'Large'),
    )

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=20, choices=SIZES, default=MEDIUM_SIZE)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='job/photos/')
    status = models.CharField(max_length=255, choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    # Step 2
    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0)
    pickup_lng = models.FloatField(default=0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=50, blank=True)

    # Step 3
    delivery_address = models.CharField(max_length=255, blank=True)
    delivery_lat = models.FloatField(default=0)
    delivery_lng = models.FloatField(default=0)
    delivery_name = models.CharField(max_length=255, blank=True)
    delivery_phone = models.CharField(max_length=50, blank=True)

    # Step 4
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    # Extra info
    pickup_photo = models.ImageField(upload_to='job/pickup_photos/', null=True, blank=True)
    pickedup_at = models.DateTimeField(null=True, blank=True)

    delivery_photo = models.ImageField(upload_to='job/delivery_photos/', null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description


class Transaction(models.Model):
    IN_STATUS = "in"
    OUT_STATUS = "out"
    STATUSES = (
        (IN_STATUS, 'In'),
        (OUT_STATUS, 'Out'),
    )

    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default=IN_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stripe_payment_intent_id
