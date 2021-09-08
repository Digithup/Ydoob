from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from DeliverySystem.models import DeliveryPerson
from catalog.models.models import Products
from helper import modelHelper

from sales.models.cart import Location
from sales.models.payment import Payment
from user.models import UserAddress
from vendors.models import Vendor

User = get_user_model()
user_models= get_user_model()

STATUS = (
    ('True', 'Yes'),
    ('False', 'NO'),
)
payment_status_choice = (
        ("Pending", "Pending"),
        ("Online Payment", "Online Payment"),
        ("Cash on delivery", "Cash on delivery")
    )

class PaymentMethods(models.Model):
    method = models.CharField(max_length=255, null=False, blank=False)
    title=models.CharField(max_length=255, null=False, blank=False)
    count = models.BigIntegerField(null=False, blank=False, default=0)
    status = models.CharField(max_length=10, choices=STATUS,default='False')
    slug = models.SlugField(null=False, max_length=128,default='nigne')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.method
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    # class Meta:
    #     ordering = ['-count']
    #     verbose_name = "Payment Method"
    #     verbose_name_plural = "Payment Methods"

STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
class Order(models.Model):

    code = models.CharField(max_length=5, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.PROTECT, null=False, blank=False)
    payment_status = models.CharField( max_length=100, null=False, blank=False, default="1", choices=payment_status_choice)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ordered = models.BooleanField(default=False)
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=False, blank=False)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

##########################################
# class OrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1, null=False, blank=False)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.product.title
#
#
# class DeliveredManager(models.Manager):
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#     def get_queryset(self):
#         return super().get_queryset().filter(status=3).order_by('created_at')
#
#
#
# class CancelledManager(models.Manager):
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#     def get_queryset(self):
#         return super().get_queryset().filter(status=4).order_by('created_at')



#
# class Orders(models.Model):
#     deliver_to_choice = (
#         (True, "Self"),
#         (False, "Other"),
#     )
#
#     payment_status_choice = (
#         ("1", "Pending"),
#         ("2", "Online Transfered/ Online Payment"),
#         ("3", "Cash In Hand")
#     )
#
#     item = models.ManyToManyField(
#         OrderProduct, blank=False, related_name="order_orderItem")
#     user = models.ForeignKey(User, null=False,
#                              blank=False, on_delete=models.PROTECT)
#     status = models.IntegerField(
#         choices=modelHelper.order_status_choice, null=False, blank=False, default=1)
#     grand_total = models.FloatField(null=True, blank=True)
#     address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
#
#     # To identify where to deliver
#     deliver_to = models.BooleanField(
#         null=False, blank=False, default=True, choices=deliver_to_choice)
#
#     # IF deliver_to == False
#     other_full_name = models.CharField(max_length=255, null=True, blank=True)
#     other_phone = models.CharField(max_length=255, null=True, blank=True)
#     other_address = models.TextField(null=True, blank=True)
#     payment_by = models.BooleanField(
#         null=False, blank=False, default=True, choices=deliver_to_choice)
#
#     # Is Required for self and other
#     district = models.ForeignKey(
#         Location, null=True, blank=True, on_delete=models.CASCADE)
#
#     direct_assign = models.ForeignKey(
#         DeliveryPerson, on_delete=models.CASCADE, null=True, blank=True, related_name="order_assigned")
#
#     any_info = models.TextField(null=True, blank=True)
#
#     payment_method = models.ForeignKey(
#         PaymentMethods, on_delete=models.PROTECT, null=False, blank=False)
#     payment_status = models.CharField(
#         max_length=100, null=False, blank=False, default="1", choices=payment_status_choice)
#
#     # If direct assign, then delivery_by = direct_assign
#     delivery_by = models.ForeignKey(DeliveryPerson, null=True,
#                                     blank=True, on_delete=models.PROTECT, related_name='order_delivery_person')
#     delivery_taken_datetime = models.DateTimeField(null=True, blank=True)
#     delivery_person_ip = models.GenericIPAddressField(
#         protocol="both", unpack_ipv4=False, null=True, blank=True)
#
#     # Orders identification
#     bill_number = models.CharField(
#         max_length=255, null=False, blank=False, unique=True)
#
#     cancelled_reason = models.TextField(
#         null=True, blank=True, help_text="Required when status=4 or Cancelled")
#
#     #if settings.MULTI_VENDOR:
#     vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=False, blank=False)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#
#     objects = models.Manager()
#     delivered_objects = DeliveredManager()
#     cancelled_objects = CancelledManager()
#
#     def __str__(self):
#         return self.user.get_full_name()
#
#     def associated_name(self):
#         return self.user.get_full_name()
#
#     def get_detail_url(self):
#         return reverse('delivery-order-details', kwargs={'id': self.id})
#
#     def delivery_person(self):
#         return self.delivery_by.user.get_full_name() if self.delivery_by else None

