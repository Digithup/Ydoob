from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import CreateView
from django.views.generic.base import RedirectView, View

from catalog.models.models import Products
from user.models import User
from vendors.decorators import seller_required, admin_required
from vendors.forms import StoreEditForm, StoreAddForm, SellerRegisterForm
from vendors.models import Store


@admin_required
# @method_decorator([login_required, admin_required], name='dispatch')
def store_list(request):
    store = Store.objects.all()
    current_user = request.user  # Access User Session information
    # setting = Store.objects.get(pk=1)
    # profile = User.objects.get(user.id)
    context = {'store': store, }
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
        #seller = request.user

        return render(request, "store-page/create-store.html",)

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
            messages.error( request,
                format_html('''You already have a store wait for activate &nbsp; &nbsp;  or learn how to sell &nbsp; 
                <a href=""> Edit</a> ''',
                            reverse('home:index', )))

            return render(request, "store-page/create-store.html", )

        else:
            store = Store(title=title_group, address=address, phone=phone, email=email,vendor_id=vendor_id)
            store.save()
            # return HttpResponse("OK")
            return render(request, 'store-page/create-success.html', )
            #return HttpResponseRedirect(reverse_lazy('home:index'))


@login_required(login_url='/home/login/')  # Check login
def vendor_dashboard(request, vendor=None):
    vendor = request.user  # Access User Session information
    owner = Store.objects.get(vendor=vendor)

    context = {'owner': owner,
               }
    return render(request, 'vendor-dashboard.html', context)

def StoreWaiting(request):
    status = Store.objects.filter(status='Disable')

    context = {'status': status,
               }
    return render(request, 'store-page/store-waiting.html', context)


def CreateSuccess(request, id):
    user = User.objects.filter(user_id=id)

    context = {'user': user,
               }
    return render(request, 'store-page/create-success.html', context)





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


@method_decorator([login_required, seller_required], name='dispatch')
def edit_store(request):
    store = Store.objects.get(id=request.store.id)
    forms = StoreEditForm(instance=store)
    if request.method == 'POST':
        forms = StoreEditForm(request.POST, request.FILES, instance=store)
        if forms.is_valid():
            forms.save()
    context = {
        'user': store,
        'forms': forms
    }
    return render(request, 'store_page.html', context)


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
