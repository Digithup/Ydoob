"""
from django.test import TestCase

# Create your tests here.
ImageFormSet = modelformset_factory(Image,
                                    form=ImageForm, extra=4)

if request.method == 'POST':
    ProductForm = ProductAddForm(request.POST)
    formset = ImageFormSet(request.POST, request.FILES,
                           queryset=ImageForm.objects.none())

    if ProductForm.is_valid() and formset.is_valid():

        ProductForm.save()

        for form in formset.cleaned_data:
            image = form['image']
            picture = ImageForm(product=ProductAddForm, image=image)
            picture.save()

        return HttpResponseRedirect('/vegetable/')
    else:
        print (ProductForm.errors, formset.errors)

else:
    VegetableForm = ProductAddForm()
    formset = ImageFormSet(queryset=Image.objects.none())

return render(request, 'vegetable/add.html',
              {'ProductForm': ProductForm, 'formset': formset},
              context_instance=RequestContext(request))




              ##############context proceesor #############

              from catalog.models.models import Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Banners
from core.models.setting import Setting, SettingMedia, SettingLang

from localization.models import Language
from vendors.models import Store, StoreMedia


def home_processors(request):
    products = Products.objects.all()
    product_list = []
    for product in products:
        product_media = ProductMedia.objects.filter(product_id=product.id, media_type=1, is_active=1).first()
        product_list.append({"product": product, "media": product_media})

    store_owner=Store.objects.filter(vendor__id=request.user.id)
    vendor_store = []
    for store in store_owner:
        vendor_media = StoreMedia.objects.filter(store_id=store_owner[0], media_type=1, is_active=1).first()
        vendor_store.append({"store": store, "vendor_media": vendor_media, })
    products_count = Products.objects.filter(seller__id=request.user.id).count()
    products = Products.objects.filter(seller__id=request.user.id)
    vendor_products_list = []
    for product in products:
        product_media = ProductMedia.objects.filter(product_id=product.id, media_type=1, is_active=1).first()
        vendor_products_list.append(
            {"product": product, "product_media": product_media, "products_count": products_count})

    try:
        return {
            'store_owner':store_owner,
            'vendor_store':vendor_store,
            'vendor_products_list':vendor_products_list,
            'setting': Setting.objects.last(),
            'setting_media': SettingMedia.objects.last(),
            'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
            'banner_left': Banners.objects.filter(media_location='left'),
            'banner_right': Banners.objects.filter(title='right'),
            'banner_down': Banners.objects.filter(title='down'),
            'manufacture': Manufacturer.objects.filter(status='True'),
            'setting_data': SettingLang.objects.all(),
            #'setting_data_en': SettingLang.objects.get(lang='en'),
            #'setting_data_ar': SettingLang.objects.get(lang='ar'),
            'index_language': Language.objects.all(),
            ####### products###########
            'product_list' : product_list , # New Products,
            'side_products': ProductMedia.objects.all().order_by('id')[:3],  # New Products
            'side_products2': ProductMedia.objects.all().order_by('product_id__title')[:3],  # New Products
            'new_products' : ProductMedia.objects.all().order_by('id')[:6]  , # New Products
            'new_products_updated': ProductMedia.objects.all().order_by('created_at')[:6],  # New Products Update
            'new_products_req': ProductMedia.objects.all().order_by('-id')[:10],  # New Products add
            'new_featured': ProductMedia.objects.all().order_by('-id')[:10],  # Featured Products
            'best_products' : ProductMedia.objects.all().order_by('?')[:6]  # Best Sellers
        }
    except BaseException as e:
        return {'setting': Setting.objects.last(),
                'setting_media': SettingMedia.objects.last(),
                'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
                'banner_left': Banners.objects.filter(media_location='left'),
                'banner_right': Banners.objects.filter(title='right'),
                'banner_down': Banners.objects.filter(title='down'),
                'manufacture': Manufacturer.objects.filter(status='True'),
                'setting_data': SettingLang.objects.all(),
                # 'setting_data_en': SettingLang.objects.get(lang='en'),
                # 'setting_data_ar': SettingLang.objects.get(lang='ar'),
                'index_language': Language.objects.all(),
                ####### products###########
                'products_media': ProductMedia.objects.all(),  # New Products,
                'side_products': ProductMedia.objects.all().order_by('id')[:3],  # New Products
                'side_products2': ProductMedia.objects.all().order_by('product_id__title')[:3],  # New Products
                'new_products': ProductMedia.objects.all().order_by('id')[:6],  # New Products
                'new_products_updated': ProductMedia.objects.all().order_by('created_at')[:6],  # New Products Update
                'new_products_req': ProductMedia.objects.all().order_by('-id')[:10],  # New Products add
                'new_featured': ProductMedia.objects.all().order_by('-id')[:10],  # Featured Products
                'best_products': ProductMedia.objects.all().order_by('?')[:6]  # Best Sellers


                },print(e);


"""
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from catalog.models.models import Categories, Products, ProductMedia, VariantDetails


def product_detailtest(request, id, slug):
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
    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = VariantDetails.objects.get(id=variant_id)  # selected product by click color radio
            colors = VariantDetails.objects.filter(product=product, size_id=variant.size_id)
            images = VariantDetails.objects.filter(product=product, size_id=variant.size_id)
            sizes = VariantDetails.objects.raw(
                'SELECT * FROM  catalog_variantdetails  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color )

        else:
            variants = VariantDetails.objects.filter(product=product)
            colors = VariantDetails.objects.filter(product=product, size_id=variants[0].size_id)
            images = VariantDetails.objects.filter(product=product, size_id=variants[0].size_id)
            sizes = VariantDetails.objects.raw(
                'SELECT * FROM  catalog_variantdetails  WHERE product_id=%s GROUP BY size_id', [id])
            variant = VariantDetails.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query,
                        'images':images})
    return render(request, 'product-details.html', context)


def ajaxcolortest(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = VariantDetails.objects.filter(product_id=productid, size_id=size_id)
        images = VariantDetails.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
            'images':images,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
