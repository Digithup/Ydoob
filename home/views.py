import json

from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from haystack.query import SearchQuerySet

from DNigne import settings
from catalog.models.models import Categories, Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Banners
from core.models.setting import Setting
from home.forms import SearchForm
from sales.models.order import ShopCart


def index(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    setting = Setting.objects.first()
    products_latest = Products.objects.all().order_by('-id')[:4]  # last 4 products
    categories = Categories.objects.all()
    product = Products.objects.all()
    banner = Banners.objects.all()
    slider_media = SliderMedia.objects.all()
    manufacture = Manufacturer.objects.filter(status='True')
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += int(rs.product.price) * int(rs.quantity)
    top_collection = Products.objects.all().order_by('-id')[:8]  # last 4 products
    products_first = Products.objects.all().order_by('id')[:8]  # first 4 products
    new_sale_products = Products.objects.all().order_by('-id')[:2]  # New Products
    new_random_products = Products.objects.all().order_by('id', 'update_at')[:4]  # New Products
    featured_products = Products.objects.all().order_by('id')[:8]  # Featured Products
    best_products = Products.objects.all().order_by('?')[:8]  # Best Sellers

    context = {
        'setting': setting,
        'categories': categories,
        'product': product,
        'design': banner,
        'manufacture': manufacture,
        # 'slider_media':slider_media,
        'shopcart': shopcart,
        'top_collection': top_collection,
        'products_first': products_first,
        'new_sale_products': new_sale_products,
        'new_random_products': new_random_products,
        'featured_products': featured_products,
        'best_products': best_products,
    }
    return render(request, 'front/index.html', context)


def CategoriesDetail(request):
    categories = Categories.objects.all()

    context = {
        'categories': categories
    }
    # return HttpResponse(1)
    return render(request, 'categories.html', context)


class CategoryDetail(DetailView):
    model = Categories
    template_name = 'category.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        #slug = kwargs["slug"]
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        #context['CategoryChilled'] = Categories.objects.filter(slug='slug')
        context['productlest'] = Products.objects.all()
        context['prodtag'] = Products.category
        return context





class ProductsListView(ListView):
    model = Products
    template_name = "front/index.html"
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
            product_media = ProductMedia.objects.filter(product_id=product.id,  ).first()
            product_list.append({"product": product, "media": product_media})

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Products._meta.get_fields()
        return context





class ProductDetailView(DetailView):
    model = Products
    template_name = 'product-details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    #context_object_name = 'productsmedia'


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

    return render(request, 'search/search.html')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Products.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def to_json(self, objects):
    return serializers.serialize('json', objects)


def search_titles(request):
    product_search = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))
    # sqs = SearchQuerySet().filter(content='foo').load_all()
    sqs = SearchQuerySet().filter(content='foo').stats('price')

    print(request.POST)

    return render(request, 'search/indexes/catalog/product_text.txt', {'product_search': product_search, 'sqs': sqs})


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
