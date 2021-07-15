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