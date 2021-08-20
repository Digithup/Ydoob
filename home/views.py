import json

import products as products
from django.core import serializers
from django.http import HttpResponse, JsonResponse, request, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import ListView, DetailView
from haystack.query import SearchQuerySet

from user.models import User
from .models import *
from DNigne import settings
from catalog.models.models import Categories, Products, ProductMedia, VariantDetails, Wishlist
from home.forms import SearchForm


# if hasattr(request.user, 'lang'):
#   request.session['django_language'] = request.user.lang


def index(request):
    all_category = Categories.objects.all()

    context = {
        'all_category': all_category
    }

    return render(request, 'front/index.html', context)


def CategoriesDetail(request):
    all_category = Categories.objects.all()

    context = {
        'all_category': all_category
    }
    # return HttpResponse(1)
    return render(request, 'categories.html', context)


def CategoryDetail(request, id, slug):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    categories = Categories.objects.all()
    category = Categories.objects.get(id=id)
    products = Products.objects.filter(category_id=id)  # default language
    category_product = []
    for product in products:
        product_media = ProductMedia.objects.filter(product=product.id, ).first()
        category_product.append({"product": product, "media": product_media})
    if defaultlang != currentlang:
        try:
            pass
            # products = Products.objects.raw(
            #     'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
            #     'FROM catalog_products as p '
            #     'LEFT JOIN product_productlang as l '
            #     'ON p.id = l.product_id '
            #     'WHERE p.category_id=%s and l.lang=%s', [id, currentlang])
        except:
            pass
        # catdata = CategoryLang.objects.get(category_id=id, lang=currentlang)

    context = {'products': products,
               'category': category,
               'categories': categories,
               'category_product': category_product}
    return render(request, 'category.html', context)


class ProductsListView(ListView):
    model = Products
    template_name = "front/index.html"
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Products
    template_name = 'product-details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        # slug = kwargs["slug"]
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product_variant'] = VariantDetails.objects.all()
        # context['CategoryChilled'] = Categories.objects.filter(slug='slug')
        return context


def product_detail(request, slug, id):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]  # en-EN
    currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0, '', currentlang)
    category = Categories.objects.all()

    product = Products.objects.get(slug=slug)

    if defaultlang != currentlang:
        try:
            prolang = Products.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'INNER JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.id=%s and l.lang=%s', [id, currentlang])
            product = prolang[0]
        except:
            pass
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end

    images = ProductMedia.objects.filter(product=product)
    # comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product, 'category': category,
               'images': images,
               }
    if product.variantdetails_set.all != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = VariantDetails.objects.get(id=variant_id)  # selected product by click color radio
            colors = VariantDetails.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = VariantDetails.objects.raw(
                'SELECT * FROM catalog_variantdetails WHERE product_id=%s group by size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = VariantDetails.objects.filter(product=product)
            colors = VariantDetails.objects.filter(product=product, )
            sizes = VariantDetails.objects.raw(
                'SELECT * FROM  catalog_variantdetails WHERE product_id=%s group by size_id', [id])
            variant = VariantDetails.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query
                        })
    return render(request, 'product-details.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = VariantDetails.objects.filter(product_id=productid, variant__title=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Products.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Products.objects.filter(title__icontains=query,category_id=catid)

            category = Categories.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Products.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def to_json(self, objects):
    return serializers.serialize('json', objects)



