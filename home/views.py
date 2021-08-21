import json

import products as products
from django.core import serializers
from django.db.models import Min, Max
from django.http import HttpResponse, JsonResponse, request, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import ListView, DetailView
from haystack.query import SearchQuerySet

from catalog.models.product_options import Color, Size
from user.models import User
from .models import *
from DNigne import settings
from catalog.models.models import Categories, Products, ProductMedia, VariantDetails, Wishlist
from home.forms import SearchForm


# if hasattr(request.user, 'lang'):
#   request.session['django_language'] = request.user.lang


def index(request):
    all_category = Categories.objects.all()
    data = Products.objects.filter(is_featured=True).order_by('-id')

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


def ProductsListView(request):
    total_data = Products.objects.count()
    data = Products.objects.all().order_by('-id')[:3]
    min_price = Products.objects.aggregate(Min('price'))
    max_price = Products.objects.aggregate(Max('price'))
    return render(request, 'category.html',
                  {
                      'data': data,
                      'total_data': total_data,
                      'min_price': min_price,
                      'max_price': max_price,
                  }
                  )


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


def to_json(self, objects):
    return serializers.serialize('json', objects)


# Search

def ProductSearch(request):
    q = request.GET['q']
    data = Products.objects.filter(title__icontains=q).order_by('-id')
    images = ProductMedia.objects.filter(product__title=q, )
    context = {'data': data,
               'images': images,
               }
    return render(request, 'search_products.html', context)


# Filter Data
def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    print(request)
    allProducts = Products.objects.all()
    allProducts = allProducts.filter(related__productdiscount__price__gt=minPrice)
    allProducts = allProducts.filter(related__productdiscount__price__lte=maxPrice)
    if len(colors) > 0:
        allProducts = allProducts.filter(variantdetails__color_id__in=colors).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(variantdetails__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'category_product': allProducts})
    return JsonResponse({'category_product': t})





# Load More
def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Products.objects.all().order_by('-id')[offset:offset + limit]
    t = render_to_string('ajax/product-list.html', {'category_product': data})
    return JsonResponse({'category_product': t}
                        )
