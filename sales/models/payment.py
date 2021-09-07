from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
user_models= get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    paid = models.BooleanField(default=False)
    stripe_charge_id = models.CharField(max_length=50)

    def __str__(self):
        return self.stripe_charge_id