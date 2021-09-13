from django import forms
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
from sales.models.orders import Order, OrderProduct


class OrderStatusForm(ModelForm):
    class Meta:

        model = OrderProduct
        fields = ['status','delivery_by','delivery_taken_datetime']
        widgets = {
            'delivery_taken_datetime': DatePickerInput(),
        }