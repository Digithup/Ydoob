import objects as objects
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect
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

@login_required(login_url='/login')  # Check login
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
            return redirect('home:index', )
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


class CreateStore(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "store-page/create-store.html", )

        else:
            if request.user.is_authenticated and request.user.seller:
                messages.error(request,
                               format_html('''You already have a store wait for activate &nbsp; &nbsp;  or learn how to sell &nbsp; 
                                <a href=""> Edit</a> ''',
                                           reverse('home:index', )))
            return redirect('user:CustomerLogin')
    def post(self, request, *args, **kwargs):
        title_group = request.POST.get("title")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        vendor_id = request.user.id
        print(request.POST)
        vendor = User.objects.filter(seller=True)
        status = Store.objects.filter(status=False ,vendor_id=vendor_id)

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
            #return HttpResponseRedirect(reverse_lazy('vendors:CreateSuccess'))


def CreateSuccess(request, ):
    is_seller = User.objects.filter(id=request.user.id ,seller=True)
    if request.user.is_authenticated and is_seller  :
        return render(request, 'store-page/create-success.html')
    else:
        return render(request, 'front/404.html')



def StoreWaiting(request):
    if not request.user.is_authenticated:
        return render(request, 'front/404.html')
    status = Store.objects.filter(status='Disable')
    context = {'status': status,
               }
    return render(request, 'store-page/store-waiting.html', context)



class VendorDashboard(View):
    def get_context_data(self, **kwargs):
        context = super(VendorDashboard, self).get_context_data(**kwargs)
        slug = kwargs["slug"]
        seller = Store.objects.filter(slug=slug)
        return context

    def get(self, request, *args, **kwargs, ):
        slug = kwargs["slug"]
        user = request.user.id
        try:
            if request.user.is_authenticated and Store.objects.get(slug=slug, vendor__id=user):
                store = Store.objects.get(slug=slug, vendor__id=user)
                store_media = StoreMedia.objects.filter(store_id=store.id).first()

                return render(request, "vendor/vendor-dashboard.html",
                              {"store": store, 'store_media': store_media})
            else:
                return render(request, 'front/404.html')
        except:
            return render(request, 'front/ErrorPage/403.html')


class EditStore(View):

    def get(self, request, *args, **kwargs, ):
        slug = kwargs["slug"]
        user = request.user.id

        try:
            if request.user.is_authenticated and Store.objects.get(slug=slug, vendor__id=user):
                store = Store.objects.get(slug=slug, vendor__id=user)
                store_media = StoreMedia.objects.filter(store_id=store.id).first()

                return render(request, "vendor/vendor-edit-store-profile.html",
                              {"store": store, 'store_media': store_media})
            else:
                return render(request, 'front/404.html')
        except:
            return render(request, 'front/ErrorPage/403.html')


    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        phone = request.POST.get("phone")
        company = request.POST.get("company")

        media_content_list = request.FILES.getlist("media_content[]")

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
        store = Store.objects.get(slug=slug)
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
            store_media = StoreMedia(store_id=store, media_content=media_url)
            store_media.save()

            i = i + 1

            print(request.POST)
            print(request)
            messages.error(request, "Error")

        return redirect(reverse('vendors:VendorDashboard',kwargs={"slug": slug},)
                        )

        # return HttpResponse("OK")

        # return HttpResponseRedirect(reverse_lazy('vendors:VendorDashboard' ))


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
        Users = self.get_account()
        exists = Users
        active = None
        context = {}
        if exists:
            active = Users.active
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
