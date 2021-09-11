from datetime import timezone

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from core.decorators import allowed_users
from core.forms.store import VendorForm
from vendors.models import Vendor


class AdminVendorList(ListView):
    model = Vendor

    template_name = 'AdminVendor/admin-vendor.html'


class VendorCreate(CreateView):
    model = Vendor
    #fields = '__all__'
    form_class = VendorForm
    template_name = 'AdminVendor/create-vendor.html'
    success_url = reverse_lazy('core:AdminVendorList')

    # @method_decorator(allowed_users(allowed_roles=['admin']))
    # def dispatch(self, *args, **kwargs):
    #     return super(PaymentMethodsCreate, self).dispatch(*args, **kwargs)

class VendorDetail(DetailView):
    model = Vendor
    template_name = 'AdminVendor/update-vendor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(VendorDetail, self).dispatch(*args, **kwargs)


class VendorUpdate(UpdateView):
    model=Vendor
    form_class=VendorForm
    template_name = 'AdminVendor/update-vendor.html'
    success_url = reverse_lazy('core:AdminVendorList')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(VendorUpdate, self).dispatch(*args, **kwargs)

class VendorDelete(DeleteView):
    model = Vendor
    fields = '__all__'
    success_url = reverse_lazy('core:AdminVendorList')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)