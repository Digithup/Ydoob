from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views import View
from requests import request

from user.models import User
from vendors import forms
from vendors.models import Store


def clean(self):
    lockup = {}

    unique_togethers = self._meta.unique_together[0]  # these could throw an error

    for field in unique_togethers:
        f = self._meta.get_field(field)

        value = getattr(self, f.attname)

        if value is None:
            continue

        if f.primary_key and not self._state.adding:
            continue

        lockup[str(field)] = value

    qs = Store.objects.filter(**lockup)

    if qs.exists and self._state.adding:
        raise ValidationError(
            format_html('''this object already exist plese edit it on <a href="{}">Edit</a>''',
                        reverse('admin:testing_snippet_change', args=(qs[0].pk,))))


class CreateStoreTest(View):
    def get(self, request, *args, **kwargs):
        print(request)
        # vendor = Store.objects.get_or_create()
        # seller = request.user

        return render(request, "store-page/create-store.html", )

    print(request)

    def post(self, request, *args, **kwargs):
        title_group = request.POST.get("title")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        vendor_id = request.user.id
        print(request.POST)
        vendor = User.objects.filter(seller=True)
        status = Store.objects.filter(status='Disable')

        if vendor and status:
            messages.error(request,
                           format_html('''You already have a store wait for activate &nbsp; &nbsp;  or learn how to sell &nbsp; 
                <a href=""> Edit</a> ''',
                                       reverse('home:index', )))

            return render(request, "store-page/create-store.html", )

        else:
            store = Store(title=title_group, address=address, phone=phone, email=email, vendor_id=vendor_id)
            store.save()
            # return HttpResponse("OK")
            return render(request, 'store-page/create-success.html', )
            # return HttpResponseRedirect(reverse_lazy('home:index'))


def become_sellers(request, id):
    forms = StoreAddForm
    if request.method == 'POST':

        print(request.POST)
        forms = StoreAddForm(request.POST, request.FILES)
        if forms.is_valid():
            store = forms.save(commit=False)
            store.vendor = request.user
            store.save()
            # Add this to check if the email already exists in your database or not
            # store.save()
            return render(request, 'store-page/create-success.html', )
    else:
        forms = StoreAddForm(request.POST, request.FILES)
        return render(request, 'store-page/create-store.html', {'forms': forms})
    return render(request, 'store-page/create-store.html', {'forms': forms})


class EditStoreTest(View  ):

    def get(self, request , *args, **kwargs , ):
        vendor_id = kwargs["vendor"]
        vendor = Store.objects.get(id=vendor_id)

        return render(request, "vendor/vendor-edit-store-profile.html",
                      {"vendor": vendor, })

    def post(self, request, *args, **kwargs):

        title = request.POST.get("title")
        brand = request.POST.get("brand")
        url_slug = request.POST.get("url_slug")
        Products_max_price = request.POST.get("Products_max_price")
        Products_discount_price = request.POST.get("Products_discount_price")
        Products_description = request.POST.get("Products_description")
        title_title_list = request.POST.getlist("title_title[]")
        details_ids = request.POST.getlist("details_id[]")
        title_details_list = request.POST.getlist("title_details[]")
        about_title_list = request.POST.getlist("about_title[]")
        about_ids = request.POST.getlist("about_id[]")
        Products_tags = request.POST.get("Products_tags")
        long_desc = request.POST.get("long_desc")






        return HttpResponseRedirect(reverse_lazy('vendors:VendorDashboard'))
