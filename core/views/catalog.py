from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView

from DNigne.settings import BASE_URL
from catalog.forms.forms import CategoryAddForm, ProductsForm, ProductMediaForm, AttributesDetailsForm, \
    OptionsDetailsForm, ColorForm, SizeForm, VariantDetailsForm
from catalog.models.models import Categories, Products, ProductMedia, ProductTags, \
    ProductTransaction, AttributesDetails, OptionsDetails, Variants
from catalog.models.product_options import Manufacturer, FiltersGroup, Filters, AttributesGroup, Attributes, Options, \
    OptionsType, Color, Size
from core.decorators import allowed_users
from core.models.setting import Setting
from localization.models.models import Language
from vendors.models import Vendor

User = get_user_model()


# @admin_required
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def AdminIndex(request):
    categories = Categories.objects.all()
    products = Products.objects.all()
    store = Vendor.objects.all()
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
        'vendor': store,
        'setting': setting,
        'index_language': index_language

    }
    return render(request, 'admin/index.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def categories(request):
    category = Categories.objects.all().annotate(product=Count('products'))
    context = {
        'category': category,
    }
    return render(request, 'catalog/category/admin-category.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def AddCategory(request):
    if request.method == "POST":
        print(request)
        form = CategoryAddForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            category_created = True
            title = form.cleaned_data['title']
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
                category_obj = Categories.objects.create(title=title,title_ar=title_ar,
                                                         keywords=keywords, parent=parent,
                                                         description=description, image=image,
                                                         slug=slug, status=status
                                                         )  # create will create as well as save too in db.

                # handling all cases of the tags
                print(request)

            category_obj.title = title
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

            return HttpResponseRedirect('/dashboard/category', category_created)

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


    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditCategory, self).dispatch(*args, **kwargs)


class DeleteCategory(DeleteView):
    model = Categories
    fields = '__all__'
    success_url = reverse_lazy('core:categories')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteCategory, self).dispatch(*args, **kwargs)


############## Products   ################

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
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

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ProductsDetailView, self).dispatch(*args, **kwargs)


class ProductsDeleted(DeleteView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('core:ProductsList')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ProductsDeleted, self).dispatch(*args, **kwargs)





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
            product_media = ProductMedia.objects.filter(product=product.id, ).first()
            product_list.append({"product": product, "media": product_media})

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Products._meta.get_fields()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ProductsList, self).dispatch(*args, **kwargs)


def load_option(request):
    option_type_id = request.GET.get('option_type')
    options = Options.objects.filter(option_type_id=option_type_id).order_by('title')
    return render(request, 'catalog/option/option_dropdown_list_options.html', {'options': options})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def ProductAdd(request):  # sourcery skip: aug-assign, convert-to-enumerate
    filters = Filters.objects.all()
    manufacturer = Manufacturer.objects.all()
    relates = Products.objects.all()
    attributes_group = request.GET.get('attributes_group')
    attribute = Attributes.objects.all()
    option_type = OptionsType.objects.all()
    option = Options.objects.all()

    if request.method == "POST":
        print(request)
        product_form = ProductsForm(request.POST or None, request.FILES or None)
        media_form = ProductMediaForm(request.POST or None, request.FILES or None)
        attribute_form = AttributesDetailsForm(request.POST or None, request.FILES or None)
        option_form = OptionsDetailsForm(request.POST or None, request.FILES or None)
        variant_form = VariantDetailsForm(request.POST or None, request.FILES or None)

        if product_form.is_valid() and media_form.is_valid() and attribute_form.is_valid() \
                and variant_form.is_valid() and option_form.is_valid():

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
            filters = request.POST.getlist('filter')
            manufacturers = request.POST.getlist('manufacturer')
            relates = request.POST.getlist('related')
            attributes = request.POST.getlist('attribute')
            attribute_details = request.POST.getlist('attribute_detail')
            options = request.POST.getlist('option')
            option_details = request.POST.getlist('option_detail')
            option_prices = request.POST.getlist('option_price')
            variant_title = request.POST.getlist('variant_title')
            variant = product_form.cleaned_data['variant']
            variant_size = request.POST.getlist('variant_size')
            variant_color = request.POST.getlist('variant_color')
            variant_price = request.POST.getlist('variant_price')
            variant_quantity = request.POST.getlist('variant_quantity')
            variant_images = request.FILES.getlist('ImageVariant')
            slug = product_form.cleaned_data['slug']
            media_content_list = request.FILES.getlist("image")
            category = Categories.objects.get(title=category)

            seller = User.objects.get(id=seller)
            product_form = None
            if not product_form:

                print(request)
                print(request.POST)

                product_form = Products(seller=seller, category=category, title=title, long_desc=long_desc,
                                        model=model, brand=brand, price=price, quantity=quantity,
                                        out_of_stock_status=out_of_stock_status, keyword=keyword,
                                        requires_shipping=requires_shipping, weight=weight,
                                        length=length, status=status, slug=slug ,variant=variant)

                product_form.save()
                j = 0
                for filter in filters:
                    product_form.filter.add(filter)
                    j = j + 1
                k = 0
                for manufacturer in manufacturers:
                    product_form.manufacturer.add(manufacturer)
                    k = k + 1
                r = 0
                for related in relates:
                    product_form.related.add(related)
                    r = r + 1

                a = 0
                for attribute_detail in attribute_details:
                    attribute_form = AttributesDetails(product=product_form, attribute_detail=attribute_detail,
                                                       attribute_id=attributes[a])
                    attribute_form.save()
                    a = a + 1

                c = 0
                for option_detail in option_details:
                    option_form = OptionsDetails(product=product_form, option_detail=option_detail,
                                                 option_price=option_prices[c], option_id=options[c])
                    option_form.save()
                    c = c + 1

                z = 0
                for variant_image in variant_images:
                    m = variant_color
                    n = ''.join(m)  # converting list into string
                    variant_color = n

                    x = variant_size
                    y = ''.join(x)  # converting list into string
                    variant_size = y

                    variant_form = Variants(product=product_form, title=variant_title[z],
                                            color=Color.objects.get(id=variant_color[z]),
                                            size=Size.objects.get(id=variant_size[z]),

                                            price=variant_price[z],
                                            quantity=variant_quantity[z], image=variant_image)
                    variant_form.save()
                    z = z + 1

                i = 0
                for image in media_content_list:
                    media_form = ProductMedia(product=product_form,
                                              image=image)
                    media_form.save()
                    i = i + 1
                    print(request.POST)
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/dashboard/products/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        product_form = ProductsForm()
        attribute_form = AttributesDetailsForm()
        media_form = ProductMediaForm()
        option_form = OptionsDetailsForm()
        variant_form = VariantDetailsForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/product/add-product.html',
                  {'manufacturer': manufacturer, 'product_form': product_form, 'media_form': media_form,
                   'filter': filters, 'option_type': option_type,
                   'relates': relates, 'attributes_group': attributes_group, 'attribute': attribute,
                   'attribute_form': attribute_form, 'option_form': option_form, 'variant_form': variant_form, }
                  )

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



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def file_upload(request):
    file = request.FILES["file"]
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    return HttpResponse('{"location":"' + BASE_URL + '' + file_url + '"}')


############## Search   ################



############## Manufacturer #######################

class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'catalog/manufacture/admin_manufacture.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerListView, self).dispatch(*args, **kwargs)


class ManufacturerDetail(DetailView):
    model = Manufacturer
    context_object_name = 'manufacturer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerDetail, self).dispatch(*args, **kwargs)


class AddManufacture(CreateView):
    model = Manufacturer
    fields = '__all__'
    template_name = 'catalog/manufacture/add-manufacture.html'
    success_url = reverse_lazy('core:Manufacturers')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddManufacture, self).dispatch(*args, **kwargs)


class EditManufacture(UpdateView):
    model = Manufacturer
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Manufacturers')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditManufacture, self).dispatch(*args, **kwargs)


class DeleteManufacture(DeleteView):
    model = Manufacturer
    fields = '__all__'
    success_url = reverse_lazy('core:Manufacturers')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteManufacture, self).dispatch(*args, **kwargs)


############## Filters #######################

class FiltersGroupListView(ListView):
    model = FiltersGroup
    template_name = 'catalog/filter/admin-filter.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(FiltersGroupListView, self).dispatch(*args, **kwargs)


class FiltersGroupDetailView(DetailView):
    model = FiltersGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(FiltersGroupDetailView, self).dispatch(*args, **kwargs)


class AddFiltersGroup(CreateView):
    model = FiltersGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/add-manufacture.html'
    success_url = reverse_lazy('core:Filters')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddFiltersGroup, self).dispatch(*args, **kwargs)


class EditFiltersGroup(UpdateView):
    model = FiltersGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Filters')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditFiltersGroup, self).dispatch(*args, **kwargs)


class DeleteFiltersGroup(DeleteView):
    model = FiltersGroup
    fields = '__all__'
    success_url = reverse_lazy('core:Filters')




    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteFiltersGroup, self).dispatch(*args, **kwargs)


class FiltersListView(ListView):
    model = Filters
    template_name = 'catalog/filter/admin-filter.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(FiltersListView, self).dispatch(*args, **kwargs)


class FilterDetailView(DetailView):
    model = Filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(FilterDetailView, self).dispatch(*args, **kwargs)


class AddFilter(View):
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddFilter, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        filters_group = FiltersGroup.objects.all()

        return render(request, "catalog/filter/add-filter.html",
                      {"filters_group": filters_group, })

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        sort_order = request.POST.get("sort_order")
        title_list = request.POST.getlist("title[]")
        sort_order_list = request.POST.getlist("sort[]")
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

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditFilter, self).dispatch(*args, **kwargs)


class DeleteFilter(DeleteView):
    model = Filters
    fields = '__all__'
    success_url = reverse_lazy('core:Filters')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteFilter, self).dispatch(*args, **kwargs)


############## Attribute  #######################

class AttributesGroupListView(ListView):
    model = AttributesGroup
    template_name = 'catalog/attribute/admin-attribute.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AttributesGroupListView, self).dispatch(*args, **kwargs)


class AttributesGroupDetailView(DetailView):
    model = AttributesGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AttributesGroupDetailView, self).dispatch(*args, **kwargs)


class AddAttributesGroup(CreateView):
    model = AttributesGroup
    fields = '__all__'
    template_name = 'catalog/attribute/add-attribute-group.html'
    success_url = reverse_lazy('core:Attributes')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddAttributesGroup, self).dispatch(*args, **kwargs)


class EditAttributesGroup(UpdateView):
    model = AttributesGroup
    fields = '__all__'
    template_name = 'catalog/manufacture/edit-manufacture.html'
    success_url = reverse_lazy('core:Attributes')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditAttributesGroup, self).dispatch(*args, **kwargs)


class DeleteAttributesGroup(DeleteView):
    model = AttributesGroup
    fields = '__all__'
    success_url = reverse_lazy('core:Attributes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteAttributesGroup, self).dispatch(*args, **kwargs)


class AttributeListView(ListView):
    model = Attributes
    template_name = 'catalog/attribute/admin-attribute.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AttributeListView, self).dispatch(*args, **kwargs)


class AttributeDetailView(DetailView):
    model = Filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AttributeDetailView, self).dispatch(*args, **kwargs)


class AddAttribute(View):

    def get(self, request, *args, **kwargs):
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

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddAttribute, self).dispatch(*args, **kwargs)


class EditAttribute(UpdateView):
    model = Attributes
    fields = '__all__'
    template_name = 'catalog/attribute/edit-attribute.html'
    success_url = reverse_lazy('core:Attributes')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditAttribute, self).dispatch(*args, **kwargs)


class DeleteAttribute(DeleteView):
    model = Attributes
    fields = '__all__'
    success_url = reverse_lazy('core:Attributes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteAttribute, self).dispatch(*args, **kwargs)


############## Options  #######################

class OptionsTypeListView(ListView):
    model = OptionsType
    template_name = 'catalog/option/admin-option.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(OptionsTypeListView, self).dispatch(*args, **kwargs)


class OptionsTypeDetailView(DetailView):
    model = OptionsType

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(OptionsTypeDetailView, self).dispatch(*args, **kwargs)


class AddOptionsType(CreateView):
    model = OptionsType
    fields = '__all__'
    template_name = 'catalog/option/add-option-type.html'
    success_url = reverse_lazy('core:Options')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddOptionsType, self).dispatch(*args, **kwargs)


class EditOptionsType(UpdateView):
    model = OptionsType
    fields = '__all__'
    template_name = 'catalog/option/edit-option.html'
    success_url = reverse_lazy('core:Attributes')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditOptionsType, self).dispatch(*args, **kwargs)


class DeleteOptionsType(DeleteView):
    model = OptionsType
    fields = '__all__'
    success_url = reverse_lazy('core:Options')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteOptionsType, self).dispatch(*args, **kwargs)


class OptionsListView(ListView):
    model = Options
    template_name = 'catalog/option/admin-option.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(OptionsListView, self).dispatch(*args, **kwargs)


class OptionDetailView(DetailView):
    model = Options

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(OptionDetailView, self).dispatch(*args, **kwargs)


class AddOption(View):
    def get(self, request, *args, **kwargs):
        print(request)
        options_type = OptionsType.objects.all()

        return render(request, "catalog/option/add-option.html",
                      {"options_type": options_type, })

    print(request)

    def post(self, request, *args, **kwargs):
        option_type = request.POST.get("option_type")
        sort_order = request.POST.get("sort_order")
        title_list = request.POST.getlist("title[]")
        sort_order_list = request.POST.getlist("sort[]")
        print(request.POST)

        options_type = OptionsType(title=option_type, sort_order=sort_order)
        options_type.save()

        j = 0
        for title_title in title_list:
            option = Options(title=title_title, sort_order=sort_order_list[j],
                             option_type=options_type)
            option.save()
            j = j + 1

        # return HttpResponse("OK")
        return HttpResponseRedirect(reverse_lazy('core:Options'))

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AddOption, self).dispatch(*args, **kwargs)


class EditOption(UpdateView):
    model = Options
    fields = '__all__'
    template_name = 'catalog/option/edit-option.html'
    success_url = reverse_lazy('core:Options')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditOption, self).dispatch(*args, **kwargs)


class DeleteOption(DeleteView):
    model = Options
    fields = '__all__'
    success_url = reverse_lazy('core:Options')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteOption, self).dispatch(*args, **kwargs)


############## Color  #######################
class VariantListView(ListView):
    model = Color
    template_name = 'catalog/variant/admin-variant.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['color'] = self.queryset
        context['size'] = Size.objects.all()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(VariantListView, self).dispatch(*args, **kwargs)


class ColorListView(ListView):
    model = Color
    template_name = 'catalog/variant/color/admin-color.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ColorListView, self).dispatch(*args, **kwargs)


class ColorDetailView(DetailView):
    model = Color

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(ColorDetailView, self).dispatch(*args, **kwargs)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def AddColor(request):  # sourcery skip: aug-assign, convert-to-enumerate

    color = Color.objects.all()
    if request.method == "POST":
        print(request)
        color_form = ColorForm(request.POST or None, request.FILES or None)
        if color_form.is_valid():
            print(request.POST)
            names = request.POST.getlist('name')
            code = request.POST.getlist('code')
            color_form = None
            if not color_form:
                print(request.POST)
                j = 0
                for name in names:
                    color_form = Color(name=name, code=code[j])
                    color_form.save()
                    j = j + 1
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/admin/Variant/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        color_form = ColorForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/variant/color/add-color.html',
                  {'color_form': color_form, 'color': color, }
                  )



    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))


class EditColor(UpdateView):
    model = Color
    fields = '__all__'
    template_name = 'catalog/variant/color/edit-color.html'
    success_url = reverse_lazy('core:Color')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditColor, self).dispatch(*args, **kwargs)


class DeleteColor(DeleteView):
    model = Color
    fields = '__all__'
    success_url = reverse_lazy('core:Color')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteColor, self).dispatch(*args, **kwargs)


############## Color  #######################

class SizeListView(ListView):
    model = Size
    template_name = 'catalog/variant/size/admin-size.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(SizeListView, self).dispatch(*args, **kwargs)


class SizeDetailView(DetailView):
    model = Size

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(SizeDetailView, self).dispatch(*args, **kwargs)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def AddSize(request):  # sourcery skip: aug-assign, convert-to-enumerate

    size = Size.objects.all()
    if request.method == "POST":
        print(request)
        Size_form = SizeForm(request.POST or None, request.FILES or None)
        if Size_form.is_valid():
            print(request.POST)
            names = request.POST.getlist('name')
            code = request.POST.getlist('code')
            Size_form = None
            if not Size_form:
                print(request.POST)
                j = 0
                for name in names:
                    Size_form = Size(name=name, code=code[j])
                    Size_form.save()
                    j = j + 1
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/admin/Variant/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        Size_form = SizeForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/variant/size/add-size.html',
                  {'Size_form': Size_form, 'size': size, }
                  )

    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))


class EditSize(UpdateView):
    model = Color
    fields = '__all__'
    template_name = 'catalog/variant/size/edit-size.html'
    success_url = reverse_lazy('core:Size')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(EditSize, self).dispatch(*args, **kwargs)


class DeleteSize(DeleteView):
    model = Color
    fields = '__all__'
    success_url = reverse_lazy('core:Variant')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSize, self).dispatch(*args, **kwargs)
