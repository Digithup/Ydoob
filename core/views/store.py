from datetime import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from core.decorators import superuser_only
from core.forms.store import AdminVendorForm
from vendors.models import Vendor

User = get_user_model()
class AdminVendorList(ListView):
    model = Vendor

    template_name = 'AdminVendor/admin-vendor.html'


class VendorCreate(CreateView):
    model = Vendor
    #fields = '__all__'
    form_class = AdminVendorForm
    template_name = 'AdminVendor/create-vendor.html'
    success_url = reverse_lazy('core:AdminVendorList')

    # @method_decorator(superuser_only)
    # def dispatch(self, *args, **kwargs):
    #     return super(PaymentMethodsCreate, self).dispatch(*args, **kwargs)

class VendorDetail(DetailView):
    model = Vendor
    template_name = 'AdminVendor/update-vendor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(superuser_only)
    def dispatch(self, *args, **kwargs):
        return super(VendorDetail, self).dispatch(*args, **kwargs)


class VendorUpdate(UpdateView):
    model=Vendor
    form_class=AdminVendorForm
    template_name = 'AdminVendor/update-vendor.html'
    success_url = reverse_lazy('core:AdminVendorList')
    @method_decorator(superuser_only)
    def dispatch(self, *args, **kwargs):
        return super(VendorUpdate, self).dispatch(*args, **kwargs)

class VendorDelete(DeleteView):
    model = Vendor
    fields = '__all__'
    success_url = reverse_lazy('core:AdminVendorList')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)