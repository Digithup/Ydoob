from django import forms
from django.contrib.auth.models import User

from DeliverySystem.models import Shipping


class BasicUserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')



class ShippingCreateStep1Form(forms.ModelForm):

  class Meta:
    model = Shipping
    fields = ('order',)

class ShippingCreateStep2Form(forms.ModelForm):
  vendor = forms.CharField(required=True)


  class Meta:
    model = Shipping
    fields = ('vendor', 'vendor_lat', 'vendor_lng')

class ShippingCreateStep3Form(forms.ModelForm):
  customer = forms.CharField(required=True)


  class Meta:
    model = Shipping
    fields = ('customer', 'customer_lat', 'customer_lng',)