from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


from helper import modelHelper
from vendors.models import Vendor

User = get_user_model()
if settings.HAS_REFERRAL_APP:
    class Referral(models.Model):
        user = models.OneToOneField(
            User, on_delete=models.CASCADE, null=False, blank=False)
        refer_code = models.CharField(max_length=255, null=False, blank=False)
        refer_url = models.URLField(null=False, blank=False, default='')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.user

        class Meta:
            verbose_name = "Referral Activation"
            verbose_name_plural = "Referral Activations"

        def user_full_name(self):
            return self.user

    class Reward(models.Model):
        referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
        points = models.BigIntegerField(null=False, blank=False, default=0)
        visited = models.BigIntegerField(null=False, blank=False, default=0)
        signed_up = models.BigIntegerField(null=False, blank=False, default=0)
        buyed = models.BigIntegerField(null=False, blank=False, default=0)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return "{} -> {}".format(self.referral.user
                                     .get_full_name(), self.points)

        class Meta:
            verbose_name = "Reward"
            verbose_name_plural = "Rewards"

        def user_full_name(self):
            return self.referral.user_full_name()

    class UserKey(models.Model):
        key = models.CharField(max_length=255, null=False,
                               blank=False, unique=True)
        referredFrom = models.ForeignKey(Referral, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return "Key: {}".format(self.key)

    class Block(models.Model):
        data = models.CharField(max_length=255, null=False, blank=False)
        data_hash = models.CharField(
            max_length=255, null=False, blank=False, unique=True)
        previous_hash = models.TextField(
            null=False, blank=False, default="00xx00")
        genesis_block = models.BooleanField(
            null=False, blank=False, choices=modelHelper.genesis_block, default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # IF GENESIS BLOCK
        user = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, null=True, blank=True)

        def __str__(self):
            return self.data


if settings.HAS_VENDOR_REFERRAL_APP:
    class VendorReferral(models.Model):
        vendor = models.OneToOneField(Vendor, null=False, blank=False, on_delete=models.CASCADE)
        refer_code = models.CharField(max_length=255, null=False, blank=False)
        refer_url = models.URLField(null=False, blank=False, default='')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.vendor

        class Meta:
            verbose_name = "Vendor Referral Activation"
            verbose_name_plural = "Vendor Referral Activations"

        def vendor_name(self):
            return self.vendor

    class VendorReward(models.Model):
        referral = models.ForeignKey(VendorReferral, on_delete=models.CASCADE)
        points = models.BigIntegerField(null=False, blank=False, default=0)
        visited = models.BigIntegerField(null=False, blank=False, default=0)
        signed_up = models.BigIntegerField(null=False, blank=False, default=0)
        buyed = models.BigIntegerField(null=False, blank=False, default=0)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return "{} -> {}".format(self.referral.vendor_name(), self.points)

        class Meta:
            verbose_name = "Vendor Reward"
            verbose_name_plural = "Vendor Rewards"

        def vendor_name(self):
            return self.referral.vendor_name()

    class VendorKey(models.Model):
        key = models.CharField(max_length=255, null=False,
                               blank=False, unique=True)
        referredFrom = models.ForeignKey(
            VendorReferral, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return "Key: {}".format(self.key)

    class VendorBlock(models.Model):
        data = models.CharField(max_length=255, null=False, blank=False)
        data_hash = models.CharField(
            max_length=255, null=False, blank=False, unique=True)
        previous_hash = models.TextField(
            null=False, blank=False, default="00xx00")
        genesis_block = models.BooleanField(
            null=False, blank=False, choices=modelHelper.genesis_block, default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # IF GENESIS BLOCK
        vendor = models.ForeignKey(
            Vendor, on_delete=models.DO_NOTHING, null=True, blank=True)

        def __str__(self):
            return self.data

