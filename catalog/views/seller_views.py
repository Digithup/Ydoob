import os
from mimetypes import guess_type
from django.conf import settings
from wsgiref.util import FileWrapper

from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View

from DNigne.mixins import AjaxRequiredMixin, SubmitBtnMixin, MultiSlugMixin, LoginRequiredMixin
from analytics.models import TagView
from catalog.forms.seller_forms import ProductsModelForm
from catalog.mixins import ProductsManagerMixin
from catalog.models.seller_models import SellerProducts, ProductsRating, MyProducts
from tags.models import Tag
from vendors.mixins import SellerAccountMixin


class ProductsRatingAjaxView(AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # if request.is_ajax():
        # raise Http404
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        Products_id = request.POST.get("Products_id")
        rating_value = request.POST.get("rating_value")
        exists = SellerProducts.objects.filter(id=Products_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

        try:
            Products_obj = SellerProducts.object.get(id=Products_id)
        except:
            Products_obj = SellerProducts.objects.filter(id=Products_id).first()

        rating_obj, rating_obj_created = ProductsRating.objects.get_or_create(
            user=user,
            Products = Products_obj
        )

        try:
            rating_obj = ProductsRating.objects.get(user=user, Products=Products_obj)
        except ProductsRating.MultipleObjectsReturned:
            rating_obj = ProductsRating.objects.filter(user=user, Products=Products_obj).first()
        except:
            rating_obj = ProductsRating()
            rating_obj.user = user
            rating_obj.Products = Products_obj
        rating_obj.rating = int(rating_value)
        myProducts = user.myProducts.Products.all()
        if Products_obj in myProducts:
            rating_obj.verified = True
        rating_obj.save()

        data = {
			"success": True
  		}
        return JsonResponse(data)

class ProductsCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
    model = SellerProducts
    template_name = "form.html"
    form_class = ProductsModelForm
    submit_btn = "Add SellerProducts"

    def form_valid(self, form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductsCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.Products.add(form.instance)


        return valid_data

class ProductsUpdateView(ProductsManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = SellerProducts
    template_name = "form.html"
    form_class = ProductsModelForm
    submit_btn = "Update SellerProducts"

    def get_initial(self):
        initial = super(ProductsUpdateView, self).get_initial()

        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        """
        tag_list = []
        for x in tags:
            tag_list.append(x.title)
        """
        return initial

    def form_valid(self, form):
        valid_data = super(ProductsUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.Products.add(self.get_object())
        return valid_data


class ProductsDetailView(MultiSlugMixin, DetailView):
    model = SellerProducts

    def get_context_data(self, *args, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        rating_avg = obj.Productsrating_set.aggregate(Avg("rating"), Count("rating"))
        context["rating_avg"] = rating_avg
        if self.request.user.is_authenticated():
            rating_obj = ProductsRating.objects.filter(user=self.request.user, Products=obj)
            if rating_obj.exists():
                context['my_rating'] = rating_obj.first().rating
            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user.id, tag)
        return context

class ProductsDownloadView(MultiSlugMixin, DetailView):
    model = SellerProducts

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myProducts.Products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(filepath)
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type='mimetype')

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)

            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404

class SellerProductsListView(SellerAccountMixin, ListView):
    model = SellerProducts
    template_name = "sellers/Products_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(SellerProductsListView, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class VendorListView(ListView):
    model = SellerProducts
    template_name = "Products/Products_list.html"

    def get_object(self):
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__name=username)
        return seller

    def get_context_data(self, *args, **kwargs):
        context = super(VendorListView, self).get_context_data(*args, **kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__name=username)
        qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class ProductsListView(ListView):
    model = SellerProducts

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductsListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class UserLibraryListView(LoginRequiredMixin, ListView):
    model = MyProducts
    template_name = "Products/library_list.html"

    def get_queryset(self, *args, **kwargs):
        obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
        qs = obj.Products.all()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

def create_view(request):
    # Form
    form = ProductsModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create SellerProducts"
    }
    return render(request, template, context)

def update_view(request, object_id=None):
    Products = get_object_or_404(SellerProducts, id=object_id)
    forms = ProductsModelForm(request.POST or None, instance=Products)
    if forms.is_valid():
        instance = forms.save(commit=False)
        # instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
            "object": Products,
            "form": forms,
            "submit_btn": "Update SellerProducts"
        }
    return render(request, template, context)

def detail_slug_view(request, slug=None):
    Products = SellerProducts.objects.get(slug=slug)
    try:
        Products = get_object_or_404(SellerProducts, slug=slug)
    except SellerProducts.MultipleObjectsReturned:
        Products = SellerProducts.objects.filter(slug=slug).order_by("-title").first()
    template = "detail_view.html"
    context = {
            "object": Products
        }
    return render(request, template, context)

def detail_view(request, object_id=None):
    Products = get_object_or_404(SellerProducts, id=object_id)
    template = "detail_view.html"
    context = {
            "object": Products
        }
    return render(request, template, context)

def list_view(request):

    queryset = SellerProducts.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
