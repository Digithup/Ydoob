from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
user_models= get_user_model()
class Notification(models.Model):
    MESSAGE = 'message'
    APPLICATION = 'application'
    NewOrder = 'new_order'
    NewRegistration ='NewRegistration'
    NewVendorCreate='NewVendorCreate'

    CHOICES = (
        (MESSAGE, 'Message'),
        (APPLICATION, 'Application'),
        (NewOrder, 'NewOrder'),
        (NewRegistration, 'NewRegistration'),
        (NewVendorCreate, 'NewVendorCreate'),

    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)
    extra_info = models.CharField(null=True, blank=True,max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']