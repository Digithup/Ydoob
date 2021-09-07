from django.forms import ModelForm

from sales.models.orders import Order, OrderProduct


class OrderStatusForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['status']