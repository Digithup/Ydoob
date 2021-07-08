from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import RedirectView, View

from catalog.models.models import Products
from user.models import User
from vendors.decorators import seller_required, admin_required
from vendors.forms import StoreEditForm, SellerRegisterForm
from vendors.models import Store, StoreMedia


@admin_required
# @method_decorator([login_required, admin_required], name='dispatch')
def store_list(request):
    stores = Store.objects.all()
    current_user = request.user  # Access User Session information
    # setting = Store.objects.get(pk=1)
    # profile = User.objects.get(user.id)
    context = {'stores': stores, }
    return render(request, 'stores-list.html', context)


class SellerRegister(CreateView):
    model = User
    form_class = SellerRegisterForm
    template_name = 'accounts/SellerRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home:index')


class CreateStore(View):
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


def CreateSuccess(request, id):
    user = User.objects.filter(user_id=id)

    context = {'user': user,
               }
    return render(request, 'store-page/create-success.html', context)


def StoreWaiting(request):
    status = Store.objects.filter(status='Disable')

    context = {'status': status,
               }
    return render(request, 'store-page/store-waiting.html', context)





class VendorDashboard(ListView):
    model = Store
    template_name = "vendor/vendor-dashboard.html"
    paginate_by = 3

    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter_val != "":
            stores = Store.objects.filter(
                Q(store_name__contains=filter_val) | Q(store_description__contains=filter_val)).order_by(order_by)
        else:
            stores = Store.objects.all().order_by(order_by)

        stores_list = []
        for store in stores:
            store_media = StoreMedia.objects.filter(store_id=store.id, media_type=1, is_active=1).first()
            stores_list.append({"store": store, "media": store_media})

        return stores_list

    def get_context_data(self, **kwargs):
        context = super(VendorDashboard, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Store._meta.get_fields()
        return context


def store_delete(request, user_id):
    store = Store.objects.get(id=user_id)
    store.is_delete = True
    store.save()
    return redirect('vendors')


# Seller catalog list and details

class SellerProductDetailRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Products, pk=kwargs['pk'])
        return obj.get_absolute_url()


# Seller transaction lists
'''''
class SellerTransactionListView(SellerAccountMixin, ListView):
	model = Transaction
	template_name = "sellers/transaction_list_view.html"

	def get_queryset(self):
		return self.get_transactions()



# Seller dashboard

class SellerDashboard(SellerAccountMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()  # NewSellerForm()
        users = self.get_account()
        exists = users
        active = None
        context = {}
        if exists:
            active = users.active
        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Seller Dashboard"
            context["products"] = self.get_products()
            transactions_today = self.get_transactions_today()
            context["transactions_today"] = transactions_today
            context["today_sales"] = self.get_today_sales()
            context["total_sales"] = self.get_total_sales()
            context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
        else:
            pass

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
'''
