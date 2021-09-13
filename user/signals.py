from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from django.contrib.auth.models import Group

from  django.dispatch import Signal

User = get_user_model()
UserModel = get_user_model()


user_logged_in = Signal(providing_args=['instance','request'])


from django.dispatch import Signal

# signal sent when users successfully recover their passwords
user_recovers_password = Signal(
    providing_args=['user', 'request']
)


def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='customer')
		instance.groups.add(group.id)

		print('Profile created!')

post_save.connect(customer_profile, sender=User)