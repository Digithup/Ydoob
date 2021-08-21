from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import RedirectView, View

from catalog.models.models import Products
from core.decorators import admin_required

from vendors.forms import SellerRegisterForm, AlreadyUserSellerRegisterForm
from vendors.models import Store, StoreMedia

User = get_user_model()
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


def AlreadyUserSellerRegister(request, slug):
    user = User.objects.get(id=request.user.id)
    forms = AlreadyUserSellerRegisterForm(instance=user)

    if request.method == 'POST':
        forms = AlreadyUserSellerRegisterForm(request.POST, request.FILES, instance=user)
        if forms.is_valid():

            seller = forms.cleaned_data['seller']

            forms = User.objects.get(id=request.user.id)

            forms.seller = seller

            forms.save()
            return redirect('home:index', user.slug)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            context = {
                'user': user,
                'forms': forms
            }
            messages.error(request, "Error")
            return render(request, 'accounts/AlreadyUserSellerRegister.html', context)

    else:
        context = {
            'user': user,
            'forms': forms
        }
        return render(request, 'accounts/AlreadyUserSellerRegister.html', context)



class dd(UpdateView):
    model = User
    form_class = AlreadyUserSellerRegisterForm
    #fields = ['phone','seller',]
    template_name = 'accounts/AlreadyUserSellerRegister.html'



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
        status = Store.objects.filter(status=False)

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


class VendorDashboard(View):

    def get_context_data(self, **kwargs):
        context = super(VendorDashboard, self).get_context_data(**kwargs)
        store_id = kwargs["store_id"]
        seller = Store.objects.filter(store_id=store_id)




        return context

    def get(self, request, *args, **kwargs, ):
        store_id = kwargs["store_id"]

        store = Store.objects.get(id=store_id)
        store_media = StoreMedia.objects.filter(store_id=store_id)
        # media_id = kwargs["store_medias"]
        # media_store = StoreMedia.objects.filter(id=media_id)

        return render(request, "vendor/vendor-dashboard.html",
                      {"store": store, 'store_media': store_media})


class EditStore(View):

    def get(self, request, *args, **kwargs, ):
        store_id = kwargs["store_id"]

        store = Store.objects.get(id=store_id)
        store_media = StoreMedia.objects.filter(store_id=store_id).first()
        # media_id = kwargs["store_medias"]
        # media_store = StoreMedia.objects.filter(id=media_id)

        return render(request, "vendor/vendor-edit-store-profile.html",
                      {"store": store, 'store_media': store_media})

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        media_content_ids = request.POST.getlist("media_content_id[]")
        about = request.POST.get("about")
        keywords = request.POST.get("keywords")
        slug = request.POST.get("slug")
        country = request.POST.get("country")
        city = request.POST.get("city")
        address = request.POST.get("address")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        twitter = request.POST.get("twitter")
        youtube = request.POST.get("youtube")
        print(request.POST)
        # status = request.POST.get("status")

        store_id = kwargs["store_id"]
        # vendor = User.objects.get(id=User.id)
        vendor = request.user.id

        store_id = kwargs["store_id"]
        store = Store.objects.get(id=store_id)
        # store.vendor=stores
        store.title = title
        store.phone = phone
        store.company = company
        store.about = about
        store.keywords = keywords
        store.slug = slug
        store.country = country
        store.city = city
        store.address = address
        store.facebook = facebook
        store.instagram = instagram
        store.twitter = twitter
        store.youtube = youtube

        store.save()
        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            store_media = StoreMedia(store_id=store, media_type=media_type_list[i], media_content=media_url)
            store_media.save()

            i = i + 1

            print(request.POST)
            print(request)
            messages.error(request, "Error")
            store_id = kwargs["store_id"]

            # media_id = kwargs["store_medias"]
            # media_store = StoreMedia.objects.filter(id=media_id)

        return redirect(reverse_lazy('vendors:VendorDashboard')
                        )

        # return HttpResponse("OK")

        # return HttpResponseRedirect(reverse_lazy('vendors:VendorDashboard' ))


def store_delete(request, user_id):
    store = Store.objects.get(id=user_id)
    store.is_delete = True
    store.save()
    return redirect('vendors')


class VendorAdminDashboard(ListView):
    model = Store
    template_name = "vendor/dashboard-bases/../templates/vendor/vendor-base/index.html"
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
        context = super(VendorAdminDashboard, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Store._meta.get_fields()
        return context


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



# Seller dashboard-bases

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

        return render(request, "sellers/dashboard-bases.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
'''
