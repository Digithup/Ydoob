import datetime
import json
from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, DetailView, UpdateView

from DNigne.settings import BASE_URL
from accounts.admin import User
from catalog.forms.forms import ProductsFullForm, CategoryAddForm
from catalog.models.models import Categories, Image, Products, ProductMedia, ProductDetails, ProductAbout, ProductTags, \
    ProductTransaction
from core.forms.forms import SearchForm
from core.models.models import Setting
from localization.models import Language
from vendors.models import Store


def index(request):
    categories = Categories.objects.all()
    category = Categories.objects.filter(id)
    products = Products.objects.all()
    store = Store.objects.all()
    setting = Setting.objects.all()
    index_language=Language.objects.filter(status=True)
    context = {
        'categories': categories,
        'category': category,
        'catalog': Products,
        'store': store,
        'setting':setting,
        'index_language':index_language

    }
    return render(request, 'admin/', context)


def categories(request):
    categories = Categories.objects.filter(status='True')

    context = {
        'categories': categories,

    }
    return render(request, 'catalog/category/category-admin.html', context)


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
            if not category_id:
                print(request)
                category_obj = Categories.objects.create(title=title, title_ar=title_ar, title_en=title_en,
                                                         keywords=keywords, parent=parent,
                                                         description=description, image=image,
                                                         slug=slug, status=status
                                                         )  # create will create as well as save too in db.

                # handling all cases of the tags
                print(request)

            for f in files:
                print(request)
                Image.objects.create(Products=category_obj, image=f)
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
        form = ProductsFullForm()
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
    template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = reverse_lazy('core:categories')


def Products_admin(request):
    products = Products.objects.filter(status='True')

    context = {
        'products': products,

    }
    return render(request, 'admin_templates/product_list.html', context)


class ProductsDetailView(DetailView):
    model = Products
    context_object_name = 'Products'
    template_name = 'catlog/../templates/catalog/Products-detail.html'


class ProductsDelete(DeleteView):
    model = Categories
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = '/admin/catalog/'

    def get_success_url(self):
        return reverse('core:Products')


def getNoteResponseData(Products_obj, tags, Products_created):
    date = datetime.datetime.now().strftime('%B') + " " + datetime.datetime.now().strftime(
        '%d') + ", " + datetime.datetime.now().strftime('%Y')
    Products_obj.refresh_from_db()
    response_data = {
        "id": Products_obj.id,
        "title": Products_obj.title,
        "keywords": Products_obj.keywords,
        "price": Products_obj.price,
        "tags": tags,
        "last_mod": date,
        "note_created": Products_created
    }
    # return JsonResponse(response_data)
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    # success_url = reverse_lazy('core:category_admin')
    return render(Products_created, 'admin/pages/../templates/catalog/category-admin.html')


def tagsInDic(tags):
    """Convert comma separated tags into dictionary"""
    last_ind = 0
    res = {}
    for i, c in enumerate(tags):
        if c == ',':
            res[tags[last_ind:i]] = 1
            last_ind = i + 1
    res[tags[last_ind:]] = 1
    return res


##################################################
#
#
#
#################################################


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
            return render(request, 'front/pages/search.html', context)

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


def to_json(self, objects):
    return serializers.serialize('json', objects)


class ProductAddView(View):
    def get(self, request, *args, **kwargs):
        print(request)
        category = Categories.objects.filter(status=True)
        sellers = User.objects.filter(seller=True)

        return render(request, "catalog/add-product.html",
                      {"categories": category, "sellers": sellers})
    print(request)
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        brand = request.POST.get("brand")
        slug = request.POST.get("slug")
        category = request.POST.get("category")
        product_description = request.POST.get("product_description")
        long_desc = request.POST.get("long_desc")
        product_max_price = request.POST.get("product_max_price")
        product_discount_price = request.POST.get("product_discount_price")
        seller = request.POST.get("seller")
        in_stock_total = request.POST.get("in_stock_total")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        title_title_list = request.POST.getlist("title_title[]")
        title_details_list = request.POST.getlist("title_details[]")
        about_title_list = request.POST.getlist("about_title[]")
        product_tags = request.POST.get("product_tags")
        print(request.POST)

        #status = request.POST.get("status")

        category = Categories.objects.get(id=category)
        seller = User.objects.get(id=seller)
        product = Products(title=title, in_stock_total=in_stock_total, slug=slug, brand=brand,
                           product_description=product_description,category=category,
                           product_max_price=product_max_price, product_discount_price=product_discount_price,
                           product_long_description=long_desc,seller=seller)
        product.save()

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            product_media = ProductMedia(product_id=product, media_type=media_type_list[i], media_content=media_url)
            product_media.save()
            i = i + 1

        j = 0
        for title_title in title_title_list:
            product_details = ProductDetails(title=title_title, title_details=title_details_list[j],
                                              product_id=product)
            product_details.save()
            j = j + 1

        for about in about_title_list:
            product_about = ProductAbout(title=about, product_id=product)
            product_about.save()

        product_tags_list = product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj = ProductTags(product_id=product, title=product_tag)
            product_tag_obj.save()

        product_transaction = ProductTransaction(product_id=product, transaction_type=1,
                                                  transaction_product_count=in_stock_total,
                                                  transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        return HttpResponse("OK")
        #return render(request, 'catalog/products-admin.html')


@csrf_exempt
def file_upload(request):
    file = request.FILES["file"]
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    return HttpResponse('{"location":"' + BASE_URL + '' + file_url + '"}')


class ProductsListView(ListView):
    model = Products
    template_name = "catalog/product/products-admin.html"
    paginate_by = 3

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
            product_media = ProductMedia.objects.filter(product_id=product.id, media_type=1, is_active=1).first()
            product_list.append({"product": product, "media": product_media})

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Products._meta.get_fields()
        return context


class ProductsEdit(View):

    def get(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        Products_details = ProductDetails.objects.filter(Products_id=Products_id)
        Products_about = ProductAbout.objects.filter(Products_id=Products_id)
        Products_tags = ProductTags.objects.filter(Products_id=Products_id)

        categories = Categories.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = Categories.objects.filter(is_active=1, category_id=category.id)
            categories_list.append({"category": category, "sub_category": sub_category})

        return render(request, "catalog/edit-Products.html",
                      {"categories": categories_list, "Products": Products, "Products_details": Products_details,
                       "Products_about": Products_about, "Products_tags": Products_tags})

    def post(self, request, *args, **kwargs):

        Products_name = request.POST.get("Products_name")
        brand = request.POST.get("brand")
        url_slug = request.POST.get("url_slug")
        sub_category = request.POST.get("sub_category")
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
        subcat_obj = Categories.objects.get(id=Categories)

        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        Products.Products_name = Products_name
        Products.url_slug = url_slug
        Products.brand = brand
        Products.subcategories_id = subcat_obj
        Products.Products_description = Products_description
        Products.Products_max_price = Products_max_price
        Products.Products_discount_price = Products_discount_price
        Products.Products_long_description = long_desc
        Products.save()

        j = 0
        for title_title in title_title_list:
            detail_id = details_ids[j]
            if detail_id == "blank" and title_title != "":
                Products_details = ProductDetails(title=title_title, title_details=title_details_list[j],
                                                   Products_id=Products)
                Products_details.save()
            else:
                if title_title != "":
                    Products_details = ProductDetails.objects.get(id=detail_id)
                    Products_details.title = title_title
                    Products_details.title_details = title_details_list[j]
                    Products_details.Products_id = Products
                    Products_details.save()
            j = j + 1

        k = 0
        for about in about_title_list:
            about_id = about_ids[k]
            if about_id == "blank" and about != "":
                Products_about = ProductAbout(title=about, Products_id=Products)
                Products_about.save()
            else:
                if about != "":
                    Products_about = ProductAbout.objects.get(id=about_id)
                    Products_about.title = about
                    Products_about.Products_id = Products
                    Products_about.save()
            k = k + 1

        ProductTags.objects.filter(Products_id=Products_id).delete()

        Products_tags_list = Products_tags.split(",")

        for Products_tag in Products_tags_list:
            Products_tag_obj = ProductTags(Products_id=Products, title=Products_tag)
            Products_tag_obj.save()

        return HttpResponse("OK")


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

        return render(request, "catalog/product/products-admin.html",
                      )


class ProductsEditMedia(View):
    def get(self, request, *args, **kwargs):
        Products_id = kwargs["Products_id"]
        products = Products.objects.get(id=Products_id)
        Products_medias = ProductMedia.objects.filter(Products_id=Products_id)
        return render(request, "catalog/product/product_edit_media.html",
                      {"Products": Products, "Products_medias": Products_medias})


class ProductsMediaDelete(View):
    def get(self, request, *args, **kwargs):
        media_id = kwargs["id"]
        Products_media = ProductMedia.objects.get(id=media_id)
        import os
        from DNigne import settings

        # It will work too Sometimes
        # Products_media.media_content.delete()
        os.remove(settings.MEDIA_ROOT.replace("\media", "") + str(Products_media.media_content).replace("/", "\\"))

        Products_id = Products_media.Products_id.id
        Products_media.delete()
        return HttpResponseRedirect(reverse("Products_edit_media", kwargs={"Products_id": Products_id}))


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


def AddProductView(request):
    if request.method == "POST":
        form = ProductsFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            product_created = True
            title = form.cleaned_data['title']
            keywords = form.cleaned_data['keywords']
            description = form.cleaned_data['description']
            thumbnail = form.cleaned_data['thumbnail']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
            image4 = form.cleaned_data['image4']
            image5 = form.cleaned_data['image5']
            image6 = form.cleaned_data['image6']
            category = form.cleaned_data['category']
            variant = form.cleaned_data['variant']
            price = form.cleaned_data['price']
            sale_price = form.cleaned_data['sale_price']
            discount = form.cleaned_data['discount']
            amount = form.cleaned_data['amount']
            min_amount = form.cleaned_data['min_amount']
            detail = form.cleaned_data['detail']
            slug = form.cleaned_data['slug']
            status = form.cleaned_data['status']
            product_id = form.cleaned_data['product_id']
            tags = tagsInDic(form.cleaned_data['tags'].strip())
            tags_dic = tags.copy()
            if not product_id:
                print(request)
                product_obj = Products.objects.create(title=title, keywords=keywords, category=category,
                                                      description=description, variant=variant,
                                                      image1=image1, image2=image2, image3=image3, image4=image4,
                                                      image5=image5, image6=image6,
                                                      thumbnail=thumbnail, price=price, sale_price=sale_price,
                                                      discount=discount,
                                                      amount=amount, min_amount=min_amount, detail=detail,
                                                      slug=slug, status=status
                                                      )  # create will create as well as save too in db.
                for k in tags.keys():
                    tag_obj, created = Products.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                print(request)
                product_obj = Products.objects.get(id=product_id)
                for t in product_obj.tags.all():
                    if t.name not in tags_dic:
                        product_obj.tags.remove(t)
                    else:  # deleting pre-existing element so that we could know what's new tags are
                        del tags_dic[t.name]
                for k, v in tags_dic.items():
                    tag_obj, created = Products.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)
                product_created = False
            for f in files:
                print(request)
                Image.objects.create(product=product_obj, image=f)
            product_obj.category = category
            product_obj.variant = variant
            product_obj.title = title
            product_obj.keywords = keywords
            product_obj.description = description
            product_obj.thumbnail = thumbnail
            product_obj.image1 = image1
            product_obj.image2 = image2
            product_obj.image3 = image3
            product_obj.image4 = image4
            product_obj.image5 = image5
            product_obj.image6 = image6
            product_obj.price = price
            product_obj.sale_price = sale_price
            product_obj.discount = discount
            product_obj.amount = amount
            product_obj.min_amount = min_amount
            product_obj.detail = detail
            product_obj.slug = slug
            product_obj.status = status
            print(request.POST)
            product_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/products', product_created)
            # return render(request,template_name='admin/pages/products-admin.html')
            # return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = ProductsFullForm()
    # return HttpResponseRedirect('/')
    return render(request, 'catalog/add-product.html', {'form': form})
