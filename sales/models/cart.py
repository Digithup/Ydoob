from django.contrib.auth import get_user_model
from django.db import models

from catalog.models.models import  Products, Variants

from vendors.models import Vendor

User = get_user_model()
class Location(models.Model):
    province = models.CharField(
        max_length=254, null=False, blank=False, default="Province 3")
    district = models.CharField(
        max_length=254, null=False, blank=False, default="Kathmandu")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.district




class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField(default='1')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.quantity} of {self.product}"
    def get_item_price(self):
        return self.quantity * self.product.price


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True,blank=True)
    variant  = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()


    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def image(self):
        return self.product.productmedia_set.all()

    @property
    def amount(self):
        return int(self.quantity) * int(self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)