from django.contrib.auth import get_user_model
from django.db import models

from sales.models.cart import Location

User = get_user_model()
user_models= get_user_model()



class DeliveryPerson(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, null=False, blank=False)
    based_on_district = models.ManyToManyField(
        Location, related_name="delivery_district", blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()
