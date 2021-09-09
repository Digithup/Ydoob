from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models.models import Products
from core.decorators import allowed_users, vendor_only
from core.forms.sales import OrderStatusForm
from sales.models.orders import Order, OrderProduct


class VendorOrdersListView(ListView):
    model = OrderProduct
    template_name = 'vendor/sales/orders/vendor-orders.html'
    paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_order'] = OrderProduct.objects.filter(vendor_id=self.request.user.id)
        context['now'] = timezone.now()
        return context
    # @method_decorator(vendor_only)
    # def dispatch(self, *args, **kwargs):
    #     return super(VendorOrdersListView, self).dispatch(*args, **kwargs)


class VendorOrderDetailView(DetailView):
    model = OrderProduct
    template_name = 'sales/orders/detail-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    # @method_decorator(allowed_users(allowed_roles=['admin']))
    # def dispatch(self, *args, **kwargs):
    #     return super(VendorOrderDetailView, self).dispatch(*args, **kwargs)


class VendorEditOrder(UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = 'vendor/sales/orders/VendorEditOrder.html'
    success_url = reverse_lazy('vendors:Order')


    # @method_decorator(vendor_only)
    # def dispatch(self, *args, **kwargs):
    #     return super(VendorEditOrder, self).dispatch(*args, **kwargs)




