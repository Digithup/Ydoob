from django import forms
from django.forms import ModelForm


from sales.models.cart import ShopCart
from sales.models.orders import PaymentMethods


class PaymentMethodsForm(ModelForm):
    class Meta:
        model = PaymentMethods
        fields = ['title','method','image','status']