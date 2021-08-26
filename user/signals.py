from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from  django.dispatch import Signal



user_logged_in = Signal(providing_args=['instance','request'])


from django.dispatch import Signal

# signal sent when users successfully recover their passwords
user_recovers_password = Signal(
    providing_args=['user', 'request']
)


#
# def customer_profile(sender, instance, created, **kwargs):
# 	if created:
# 		group = Group.objects.get(name='customer')
# 		instance.groups.add(group)
# 		Customer.objects.create(
# 			user=instance,
# 			name=instance.username,
# 			)
# 		print('Profile created!')
#
# post_save.connect(customer_profile, sender=User)