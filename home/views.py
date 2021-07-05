import datetime
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from haystack import indexes
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean

from DNigne import settings
from catalog.models.models import Categories, Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import Slider, SliderMedia, Banners
from core.models.setting import Setting

from home.forms import SearchForm
from sales.models.order import ShopCart

from vendors.models import Store


def index(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    setting = Setting.objects.first()
    products_latest = Products.objects.all().order_by('-id')[:4]  # last 4 products
    categories = Categories.objects.all()
    products = Products.objects.all()

    store = Store.objects.all()

    banner= Banners.objects.all()
    slider_media = SliderMedia.objects.all()
    manufacture =Manufacturer.objects.filter(status='True')
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    top_collection = Products.objects.all().order_by('-id')[:8]  # last 4 products
    products_first = Products.objects.all().order_by('id')[:8]  # first 4 products

    new_sale_products = Products.objects.all().order_by('-id')[:2]  # New Products
    new_random_products = Products.objects.all().order_by('id', 'update_at')[:4]  # New Products
    featured_products = Products.objects.all().order_by('id')[:8]  # Featured Products
    best_products = Products.objects.all().order_by('?')[:8]  # Best Sellers

    context = {
        'setting': setting,
        'categories': categories,
        'products': products,

        'store': store,
        'banner': banner,

        'manufacture':manufacture,
        #'slider_media':slider_media,
        'shopcart': shopcart,
        'top_collection': top_collection,
        'products_first': products_first,

        'new_sale_products': new_sale_products,
        'new_random_products': new_random_products,
        'featured_products': featured_products,
        'best_products': best_products,
    }
    return render(request, 'front/index.html', context)


def categories(request):
    categories = Categories.objects.all()

    context = {
        'categories': categories
    }
    # return HttpResponse(1)
    return render(request, 'front/pages/category_list.html', context)

class CategoriesView(ListView):
    template_name = 'home_category.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Products.objects.all()



class ProductsHomeListView(ListView):
    model = Products
    template_name = "catalog/product/admin-products.html"
    paginate_by = 12

class ProductDetailView(DetailView):
    model = Products
    template_name = 'product-no-sidebar.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['productlest'] = Products.objects.all()
        context['prodtag'] = Products.category
        return context


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

    return render(request, 'front/pages/search.html')


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

    return render(request, 'search/search.html', {'product_search': product_search, 'sqs': sqs})


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
