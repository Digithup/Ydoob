from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from DeliverySystem.models import Courier
from core.decorators import allowed_users
from core.forms.delivery import AdminCourierForm
from core.forms.sales import OrderStatusForm
from sales.models.orders import Order


class CourierListView(ListView):
    model = Courier
    template_name = 'delivery/admin-delivery.html'
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CourierListView, self).dispatch(*args, **kwargs)


class CourierCreate(CreateView):
    model = Courier
    form_class = AdminCourierForm

    template_name = 'delivery/admin-add-delivery.html'
    success_url = reverse_lazy('core:Courier')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CourierCreate, self).dispatch(*args, **kwargs)


class CourierDetail(DetailView):
    model = Courier
    template_name = 'sales/orders/detail-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CourierDetail, self).dispatch(*args, **kwargs)


class CourierEdit(UpdateView):
    model = Courier
    form_class = AdminCourierForm

    template_name = 'sales/orders/admin_edit-order.html'
    success_url = reverse_lazy('core:Order')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CourierEdit, self).dispatch(*args, **kwargs)
