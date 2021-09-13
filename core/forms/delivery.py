from django.forms import ModelForm

from DeliverySystem.models import Courier


class AdminCourierForm(ModelForm):
    class Meta:
        model = Courier
        fields = ['user','status']
