from django.core import serializers
from django.db.models import Min, Max
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView

from DNigne import settings
from catalog.models.models import Categories, Products, ProductMedia, Variants


# if hasattr(request.user, 'lang'):
#   request.session['django_language'] = request.user.lang
from vendors.models import Vendor


def error403(request):
    return render(request, 'front/ErrorPage/403.html', )

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
    return render(request, 'Category/categories.html', context)


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
    return render(request, 'Category/category.html', context)


def ProductsListView(request):
    total_data = Products.objects.count()
    data = Products.objects.all().order_by('-id')[:3]
    min_price = Products.objects.aggregate(Min('price'))
    max_price = Products.objects.aggregate(Max('price'))
    return render(request, 'Category/category.html',
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
        context['product_variant'] = Variants.objects.all()
        # context['CategoryChilled'] = Categories.objects.filter(slug='slug')
        return context


def product_detail(request, id, slug):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]  # en-EN
    currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0, '', currentlang)
    category = Categories.objects.all()

    product = Products.objects.get(slug=slug)
    try:
        store = Vendor.objects.get(vendor__id=product.seller.id)
    except:
        store = None


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
               'images': images,'vendor':store,
               }
    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product=product, size_id=variant.size_id)
            images = Variants.objects.filter(product=product, size_id=variant.size_id)

            sizes = Variants.objects.raw(
                'SELECT * FROM  catalog_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color )

        else:
            variants = Variants.objects.filter(product=product)
            colors = Variants.objects.filter(product=product, size_id=variants[0].size_id)
            images = Variants.objects.filter(product=product, size_id=variants[0].size_id)

            sizes = Variants.objects.raw(
                'SELECT * FROM  catalog_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query,
                        'images':images,'vendor':store,})
    return render(request, 'Products-Page/product-detail-finich1.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':

        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        images = Variants.objects.filter(product_id=productid, size_id=size_id)
        prices = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
            'images':images,
            'prices':prices
        }
        print(request)
        data = {'rendered_table': render_to_string('Products-Page/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def ajaxprice(request):
    data = {}
    if request.POST.get('action') == 'post':

        size_id = request.POST.get('size')
        productid = request.POST.get('productid')

        prices = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,

            'prices':prices
        }
        print(request)
        data = {'rendered_table': render_to_string('Products-Page/price_list.html', context=context)}
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
    return render(request, 'Search/search_products.html', context)


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
def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)