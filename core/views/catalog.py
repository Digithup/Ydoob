import datetime
import json

from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView

from DNigne.settings import BASE_URL
from catalog.forms.forms import CategoryAddForm, ProductsForm, ProductMediaForm
from catalog.models.models import Categories, Products, ProductMedia, ProductTags, \
    ProductTransaction
from catalog.models.product_options import Manufacturer, FiltersGroup, Filters, AttributesGroup, Attributes
from core.forms.forms import SearchForm
from core.models.setting import Setting
from localization.models import Language
from user.admin import User
from vendors.models import Store


def index(request):

    categories = Categories.objects.all()
    products = Products.objects.all()
    store = Store.objects.all()
    setting = Setting.objects.all()
    index_language = []
    if index_language is not None:
        index_language = Language.objects.filter(status=True)
    else:
        pass
    context = {
        'categories': categories,
        'products': products,
        'catalog': Products,
        'store': store,
        'setting': setting,
        'index_language': index_language

    }
    return render(request, 'admin/', context)


def categories(request):
    categories = Categories.objects.filter(status='True')

    context = {
        'categories': categories,

    }
    return render(request, 'catalog/category/admin-category.html', context)


def AddCategory(request):
    if request.method == "POST":
        print(request)
        form = CategoryAddForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            category_created = True
            title = form.cleaned_data['title']
            title_en = form.cleaned_data['title_en']
            title_ar = form.cleaned_data['title_ar']
            keywords = form.cleaned_data['keywords']
            description = form.cleaned_data['description']
            parent = form.cleaned_data['parent']
            image = form.cleaned_data['image']
            slug = form.cleaned_data['slug']
            status = form.cleaned_data['status']
            category_id = form.cleaned_data['category_id']
            category_obj = None
            if not category_id:
                print(request)
                category_obj = Categories.objects.create(title=title, title_ar=title_ar, title_en=title_en,
                                                         keywords=keywords, parent=parent,
                                                         description=description, image=image,
                                                         slug=slug, status=status
                                                         )  # create will create as well as save too in db.

                # handling all cases of the tags
                print(request)

            category_obj.title = title
            category_obj.title_en = title_en
            category_obj.title_ar = title_ar
            category_obj.keywords = keywords
            category_obj.description = description
            category_obj.image = image
            category_obj.parent = parent
            category_obj.slug = slug
            category_obj.status = status
            print(request.POST)
            messages.success(request, "SUCCESS")
            category_obj.save()  # last_modified field won't update on changing other model field, save() trigger change
            # return reverse('core:catalog')

            return HttpResponseRedirect('/admin/category', category_created)

            # return render(request,template_name='admin/pages/Products-admin.html')
            # return getNoteResponseData(Products_obj, tags, Products_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = CategoryAddForm()
    # return HttpResponseRedirect('/')
    return render(request, 'catalog/category/add-category.html', {'form': form})


class EditCategory(UpdateView):
    model = Categories
    fields = '__all__'
    template_name = 'catalog/category/edit-category.html'
    success_url = reverse_lazy('core:categories')


class DeleteCategory(DeleteView):
    model = Categories
    fields = '__all__'

    success_url = reverse_lazy('core:categories')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


############## Products   ################
def Products_admin(request):
    products = Products.objects.filter(status='True')

    context = {
        'products': products,

    }
    return render(request, 'admin_templates/product_list.html', context)


class ProductsDetailView(DetailView):
    model = Products
    context_object_name = 'Products'
    template_name = 'catalog/product/product-detail.html'


class ProductsDeleted(DeleteView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('core:Products_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


def getNoteResponseData(Product, tags, Products_created):
    date = datetime.datetime.now().strftime('%B') + " " + datetime.datetime.now().strftime(
        '%d') + ", " + datetime.datetime.now().strftime('%Y')
    Product.refresh_from_db()
    response_data = {
        "id": Product.id,
        "title": Product.title,
        "keywords": Product.product_description,
        "price": Products.price,
        "tags": tags,
        "last_mod": date,

    }
    # return JsonResponse(response_data)
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    # success_url = reverse_lazy('core:category_admin')
    return render(Products_created, 'catalog/product/admin-products.html')


class ProductsList(ListView):
    model = Products
    template_name = "catalog/product/admin-products.html"
    paginate_by = 12

    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter_val != "":
            products = Products.objects.filter(
                Q(Products_name__contains=filter_val) | Q(Products_description__contains=filter_val)).order_by(order_by)
        else:
            products = Products.objects.all().order_by(order_by)
        product_list = []
        for product in products:
            product_media = ProductMedia.objects.filter(product=product.id,).first()
            product_list.append({"product": product, "media": product_media})

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Products._meta.get_fields()
        return context



def ProductAdd(request):
    # 'extra' means the number of photos that you can upload   ^
    if request.method == "POST":

        print(request)
        product_form = ProductsForm(request.POST or None, request.FILES or None)
        media_form = ProductMediaForm(request.POST or None, request.FILES or None)

        if product_form.is_valid() and media_form.is_valid():
            print(request.POST)
            product_created = True
            seller = request.user.id
            category = product_form.cleaned_data['category']
            title = product_form.cleaned_data['title']
            long_desc = product_form.cleaned_data['long_desc']
            keyword = product_form.cleaned_data['keyword']
            model = product_form.cleaned_data['model']
            brand = product_form.cleaned_data['brand']
            price = product_form.cleaned_data['price']
            quantity = product_form.cleaned_data['quantity']
            out_of_stock_status = product_form.cleaned_data['out_of_stock_status']
            requires_shipping = product_form.cleaned_data['requires_shipping']
            weight = product_form.cleaned_data['weight']
            length = product_form.cleaned_data['length']
            status = product_form.cleaned_data['status']
            slug = product_form.cleaned_data['slug']
            media_content_list = request.FILES.getlist("image")

            category = Categories.objects.get(title=category)
            seller = User.objects.get(id=seller)

            product_form = None

            if not product_form:

                print(request)
                print(request.POST)

                product_form = Products(seller=seller, category=category, title=title,
                                        long_desc=long_desc,
                                        model=model, brand=brand, price=price, quantity=quantity,
                                        out_of_stock_status=out_of_stock_status, keyword=keyword,

                                        requires_shipping=requires_shipping, weight=weight, length=length,
                                        status=status,
                                        slug=slug)

                product_form.save()
                i = 0

                for image in media_content_list:
                    media_form = ProductMedia(product=product_form,
                                              Image=image)
                    media_form.save()
                    i = i + 1
                    print(request.POST)
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/admin/products/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        product_form = ProductsForm()

        media_form = ProductMediaForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/product/add-product.html',
                  {'product_form': product_form, 'media_form': media_form})

    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))

class ProductUpdate(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = Products.objects.get(id=product_id)

        product_tags = ProductTags.objects.filter(product_id=product_id)

        return render(request, "catalog/product/edit-product.html",
                      {"categories": categories, "product": product,
                       "Product_tags": product_tags})

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
        categories = Categories.objects.get(id=Categories)

        Products_id = kwargs["product_id"]
        products = Products.objects.get(id=id)
        Products.title = title
        Products.url_slug = url_slug
        Products.brand = brand
        Products.Products_description = Products_description
        Products.Products_max_price = Products_max_price
        Products.Products_discount_price = Products_discount_price
        Products.Products_long_description = long_desc
        Products.save()

        ProductTags.objects.filter(Products_id=Products_id).delete()

        Products_tags_list = Products_tags.split(",")

        for Products_tag in Products_tags_list:
            Products_tag_obj = ProductTags(Products_id=Products, title=Products_tag)
            Products_tag_obj.save()

        return HttpResponseRedirect(reverse_lazy('core:Products_list'))


class ProductsAddMedia(View):
    def get(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        return render(request, "catalog/product/product_add_media.html", {"Products": Products})

    def post(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            Products_media = ProductMedia(Products_id=Products, media_type=media_type_list[i], media_content=media_url)
            Products_media.save()
            i = i + 1

        return render(request, "catalog/product/admin-products.html",
                      )


class ProductEditMedia(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = Products.objects.get(id=product_id)
        product_medias = ProductMedia.objects.filter(product_id=product_id)
        return render(request, "admin_templates/product_edit_media.html",
                      {"product": product, "product_medias": product_medias})


class ProductMediaDelete(View):
    def get(self, request, *args, **kwargs):
        media_id = kwargs["id"]
        product_media = ProductMedia.objects.get(id=media_id)
        import os
        from DNigne import settings

        # It will work too Sometimes
        # product_media.media_content.delete()
        os.remove(settings.MEDIA_ROOT.replace("\media", "") + str(product_media.media_content).replace("/", "\\"))

        product_id = product_media.product_id.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media", kwargs={"product_id": product_id}))


class ProductsAddStocks(View):
    def get(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        return render(request, "catalog/product/product_add_stocks.html", {"Products": Products})

    def post(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        new_instock = request.POST.get("add_stocks")
        products = Products.objects.get(id=Products_id)
        old_stocks = Products.in_stock_total
        new_stocks = int(new_instock) + int(old_stocks)
        Products.in_stock_total = new_stocks
        Products.save()

        Products_obj = Products.objects.get(id=Products_id)
        Products_transaction = ProductTransaction(Products_id=Products_obj, transaction_Products_count=new_instock,
                                                  transaction_description="New Products Added", transaction_type=1)
        Products_transaction.save()
        return HttpResponseRedirect(reverse("Products_add_stocks", kwargs={"Products_id": Products_id}))


def to_json(self, objects):
    return serializers.serialize('json', objects)


@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+BASE_URL+''+file_url+'"}')



############## Search   ################

def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Products.objects.filter(
                    title__icontains=query)  # SELECT * FROM catalog WHERE title LIKE '%query%'
            else:
                products = Products.objects.filter(title__icontains=query, category_id=catid)

            category = Categories.objects.all()
            context = {'products': products, 'query': query,
                       'category': category}
            return render(request, 'search/search.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Products.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            Products_json = {}
            Products_json = rs.title + " > " + rs.category.title
            results.append(Products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


############## Manufacturer #######################

class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'catalog/manufacture/admin_manufacture.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ManufacturerDetailView(DetailView):
    model = Manufacturer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AddManufacture(CreateView):
    model = Manufacturer
    fields = '__all__'
    template_name = 'catalog/manufacture/add-manufacture.html'
    success_url = reverse_lazy('core:Manufacturers')


class EditManufacture(UpdateView):
    model = Manufacturer
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Manufacturers')


class DeleteManufacture(DeleteView):
    model = Manufacturer
    fields = '__all__'
    success_url = reverse_lazy('core:Manufacturers')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


############## Filters #######################

class FiltersGroupListView(ListView):
    model = FiltersGroup
    template_name = 'catalog/filter/admin-filter.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class FiltersGroupDetailView(DetailView):
    model = FiltersGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AddFiltersGroup(CreateView):
    model = FiltersGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/add-manufacture.html'
    success_url = reverse_lazy('core:Filters')


class EditFiltersGroup(UpdateView):
    model = FiltersGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Filters')


class DeleteFiltersGroup(DeleteView):
    model = FiltersGroup
    fields = '__all__'
    success_url = reverse_lazy('core:Filters')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class FiltersListView(ListView):
    model = Filters
    template_name = 'catalog/filter/admin-filter.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class FilterDetailView(DetailView):
    model = Filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AddFilter(View):
    def get(self, request, *args, **kwargs):
        print(request)
        filters_group = FiltersGroup.objects.all()

        return render(request, "catalog/filter/add-filter.html",
                      {"filters_group": filters_group, })

    print(request)

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        sort_order = request.POST.get("sort_order")
        title_list = request.POST.getlist("title[]")
        sort_order_list = request.POST.getlist("sort[]")
        print(request.POST)

        filters_group = FiltersGroup(title=title, sort_order=sort_order)
        filters_group.save()

        j = 0
        for title_title in title_list:
            filter = Filters(title=title_title, sort_order=sort_order_list[j],
                             filter_group=filters_group)
            filter.save()
            j = j + 1

        # return HttpResponse("OK")
        return HttpResponseRedirect(reverse_lazy('core:Filters'))


class EditFilter(UpdateView):
    model = Filters
    fields = '__all__'
    template_name = 'catalog/filter/edit-filter.html'
    success_url = reverse_lazy('core:Filters')


class DeleteFilter(DeleteView):
    model = Filters
    fields = '__all__'
    success_url = reverse_lazy('core:Filters')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


############## Attribute  #######################

class AttributesGroupListView(ListView):
    model = AttributesGroup
    template_name = 'catalog/attribute/admin-attribute.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AttributesGroupDetailView(DetailView):
    model = AttributesGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AddAttributesGroup(CreateView):
    model = AttributesGroup
    fields = '__all__'
    template_name = 'catalog/attribute/add-attribute-group.html'
    success_url = reverse_lazy('core:Attributes')


class EditAttributesGroup(UpdateView):
    model = AttributesGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Attributes')


class DeleteAttributesGroup(DeleteView):
    model = AttributesGroup
    fields = '__all__'
    success_url = reverse_lazy('core:Attributes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AttributeListView(ListView):
    model = Attributes
    template_name = 'catalog/attribute/admin-attribute.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AttributeDetailView(DetailView):
    model = Filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AddAttribute(View):
    def get(self, request, *args, **kwargs):
        print(request)
        attributes_group = AttributesGroup.objects.all()

        return render(request, "catalog/attribute/add-attribute.html",
                      {"attributes_group": attributes_group, })

    print(request)

    def post(self, request, *args, **kwargs):
        title_group = request.POST.get("title")
        sort_order = request.POST.get("sort_order")
        title_list = request.POST.getlist("title[]")
        sort_order_list = request.POST.getlist("sort[]")
        print(request.POST)

        attribute_group = AttributesGroup(title=title_group, sort_order=sort_order)
        attribute_group.save()

        j = 0
        for title_title in title_list:
            attribute = Attributes(title=title_title, sort_order=sort_order_list[j],
                                   attributes_group=attribute_group)
            attribute.save()
            j = j + 1

        # return HttpResponse("OK")
        return HttpResponseRedirect(reverse_lazy('core:Attributes'))


class EditAttribute(UpdateView):
    model = Attributes
    fields = '__all__'
    template_name = 'catalog/attribute/edit-attribute.html'
    success_url = reverse_lazy('core:Attributes')


class DeleteAttribute(DeleteView):
    model = Attributes
    fields = '__all__'
    success_url = reverse_lazy('core:Attributes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
