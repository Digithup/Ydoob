from django.forms import ModelForm

from sales.models.order import Order


class OrderStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']