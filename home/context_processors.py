from catalog.models.models import Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Banners
from core.models.setting import Setting, SettingLang

from localization.models import Language
from vendors.models import Store, StoreMedia



def home_processors(request):

    products = Products.objects.all()
    product_list = []
    for product in products:
        product_media = ProductMedia.objects.filter(product=product.id,).first()
        product_list.append({"product": product, "media": product_media})

        ##############Vendor###########  ##############Vendor###########

    store_owner=Store.objects.filter(vendor__id=request.user.id)
    vendor_store = []
    for store in store_owner:
        vendor_media = StoreMedia.objects.filter(store_id=store_owner[0],).first()
        vendor_store.append({"store": store, "vendor_media": vendor_media, })
    products_count = Products.objects.filter(seller__id=request.user.id).count()
    products = Products.objects.filter(seller__id=request.user.id)
    vendor_products_list = []
    for product in products:
        product_media = ProductMedia.objects.filter(product=product.id, ).first()
        vendor_products_list.append(
            {"product": product, "product_media": product_media, "products_count": products_count})

        ##############Vendor###########  ##############Vendor###########

    try:
        return {
            'store_owner':store_owner,
            'vendor_store':vendor_store,
            'vendor_products_list':vendor_products_list,
            'setting': Setting.objects.last(),

            'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
            'banner_left': Banners.objects.filter(media_location='left'),
            'banner_right': Banners.objects.filter(title='right'),
            'banner_down': Banners.objects.filter(title='down'),
            'manufacture': Manufacturer.objects.filter(status='True'),
            'setting_data': SettingLang.objects.get(lang=request.LANGUAGE_CODE),
            'index_language': Language.objects.all(),
            ####### products###########
            'product_list' : product_list , # New Products,
            'side_products': product_list,  # New Products
            'side_products2': product_list,  # New Products
            'new_products' : product_list , # New Products
            'new_products_updated': product_list,  # New Products Update
            'new_products_req': product_list,  # New Products add
            'new_featured': product_list,  # Featured Products
            'best_products' : product_list,  # Best Sellers
            'categories_product':product_list, # categories_product
            'products_related ': product_list,  # related_product
        }
    except BaseException as e:
        return {'setting': Setting.objects.last(),

                'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
                'banner_left': Banners.objects.filter(media_location='left'),
                'banner_right': Banners.objects.filter(title='right'),
                'banner_down': Banners.objects.filter(title='down'),
                'manufacture': Manufacturer.objects.filter(status='True'),
                'setting_data': SettingLang.objects.all(),

                'index_language': Language.objects.all(),
                ####### products###########
                'products_media': Products.objects.all(),  # New Products,
                'side_products': product_list,  # New Products
                'side_products2': product_list,  # New Products
                'new_products': product_list,  # New Products
                'new_products_updated': product_list,  # New Products Update
                'new_products_req': product_list,  # New Products add
                'new_featured': product_list,  # Featured Products
                'best_products': product_list,  # Best Sellers
                'categories_product': product_list, # categories_product
                'products_related ': product_list,  # related_product


                },print(e);

