
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from catalog.models.models import Categories, Products, ProductMedia, Variants
from vendors.models import Store


def product_detailtest(request, id, slug):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]  # en-EN
    currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0, '', currentlang)
    category = Categories.objects.all()

    product = Products.objects.get(slug=slug)
    store=Store.objects.get(vendor__id=product.seller.id)

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
               'images': images,'store':store,
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
                        'images':images,'store':store,})
    return render(request, 'product-page.html', context)


def ajaxcolortest(request):
    data = {}
    if request.POST.get('action') == 'post':

        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        images = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
            'images':images,
        }
        print(request)
        data = {'rendered_table': render_to_string('Products-Page/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
