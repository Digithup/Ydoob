from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.decorators import superuser_only
from core.forms.sales import OrderStatusForm
from sales.models.orders import Order


class OrdersListView(ListView):
    model = Order
    template_name = 'sales/orders/admin-orders.html'
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(superuser_only)
    def dispatch(self, *args, **kwargs):
        return super(OrdersListView, self).dispatch(*args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'sales/orders/detail-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(superuser_only)
    def dispatch(self, *args, **kwargs):
        return super(OrderDetailView, self).dispatch(*args, **kwargs)


class EditOrder(UpdateView):
    model = Order
    form_class = OrderStatusForm

    template_name = 'sales/orders/admin_edit-order.html'
    success_url = reverse_lazy('core:Order')

    @method_decorator(superuser_only)
    def dispatch(self, *args, **kwargs):
        return super(EditOrder, self).dispatch(*args, **kwargs)
