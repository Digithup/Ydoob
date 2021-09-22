import item as item
from django import forms
from django.forms import ModelForm


from sales.models.cart import ShopCart
from sales.models.orders import Order, OrderProduct
from vendors.models import Vendor


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity',]


class CheckoutForm(ModelForm):

    class Meta:
        model = Order
        fields = [ 'address','payment_method' ]
        widgets = {
            'payment_method': forms.RadioSelect(attrs={'class': 'custom-select'}),
            'address': forms.RadioSelect(attrs={'class': 'custom-select'}),
        }


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class OrderProductForm(ModelForm):

    class Meta:
        model = OrderProduct
        fields = '__all__'


# class CheckoutForm(ModelForm):


    # class Meta:
    #     model = Orders
    #     fields = [  'address','payment_method']
    #     widgets = {
    #                 'payment_method': forms.RadioSelect(attrs={'class': 'custom-select'}),
    #                 'address': forms.RadioSelect(attrs={'class': 'custom-select'}),
    #                }
