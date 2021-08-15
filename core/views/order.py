from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms.sales import OrderStatusForm
from sales.models.order import Order


class OrdersListView(ListView):
    model = Order
    template_name = 'sales/orders/admin-orders.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'sales/orders/detail-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EditOrder(UpdateView):
    model = Order
    form_class = OrderStatusForm

    template_name = 'sales/orders/edit-order.html'
    success_url = reverse_lazy('core:Orders')




