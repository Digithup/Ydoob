from django.forms import ModelForm

from sales.models.orders import Order


class OrderStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']