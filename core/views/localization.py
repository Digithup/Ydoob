from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from core.decorators import allowed_users
from core.forms.localization import AdminCountryForm
from localization.models.models import Country, Governorates


class CountryListView(ListView):
    model = Country
    template_name = 'localization/country/admin-country.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


class CountryDetailView(DetailView):
    model = Country

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CountryDetailView, self).dispatch(*args, **kwargs)

class CountryCreate(CreateView):
    model = Country
    form_class = AdminCountryForm
    template_name = 'localization/country/add-country.html'
    success_url = reverse_lazy('core:CountryListView')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CountryCreate, self).dispatch(*args, **kwargs)


class CountryEdit(UpdateView):
    model = Country
    fields = '__all__'
    template_name = 'localization/country/edit-country.html'
    success_url = reverse_lazy('core:CountryListView')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CountryEdit, self).dispatch(*args, **kwargs)


class CountryDelete(DeleteView):
    model = Country
    fields = '__all__'
    success_url = reverse_lazy('core:CountryListView')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(CountryDelete, self).dispatch(*args, **kwargs)





class GovernoratesListView(ListView):
    model = Governorates
    template_name = 'localization/country/admin-country.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(GovernoratesListView, self).dispatch(*args, **kwargs)


class GovernoratesDetailView(DetailView):
    model = Governorates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(GovernoratesDetailView, self).dispatch(*args, **kwargs)

class GovernoratesCreate(CreateView):
    model = Governorates
    form_class = AdminCountryForm
    template_name = 'localization/country/add-country.html'
    success_url = reverse_lazy('core:CountryListView')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(GovernoratesCreate, self).dispatch(*args, **kwargs)


class GovernoratesEdit(UpdateView):
    model = Governorates
    fields = '__all__'
    template_name = 'localization/country/edit-country.html'
    success_url = reverse_lazy('core:CountryListView')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(GovernoratesEdit, self).dispatch(*args, **kwargs)


class GovernoratesDelete(DeleteView):
    model = Governorates
    fields = '__all__'
    success_url = reverse_lazy('core:CountryListView')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(GovernoratesDelete, self).dispatch(*args, **kwargs)