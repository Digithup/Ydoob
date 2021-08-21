from django.db.models import Min, Max

from catalog.models.models import Products, ProductMedia, Categories, Wishlist
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Banners
from core.models.setting import SettingLang, Setting
from localization.models import Language

from user.models import UserAddress
from vendors.models import Store, StoreMedia


def home_processors(request):
    products = Products.objects.all()
    product_list = []
    for product in products:
        product_media = ProductMedia.objects.filter(product=product.id, ).first()
        product_list.append({"product": product, "media": product_media})

        ##############Vendor###########  ##############Vendor###########

    store_owner = Store.objects.filter(vendor__id=request.user.id)
    vendor_store = []
    for store in store_owner:
        vendor_media = StoreMedia.objects.filter(store_id=store_owner[0], ).first()
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
            'setting': Setting.objects.last(),

            'setting_data_en': SettingLang.objects.get(lang='en'),
            'setting_data_ar': SettingLang.objects.get(lang='ar'),
            'index_language': Language.objects.all(),

            'store_owner': store_owner,
            'vendor_store': vendor_store,
            'vendor_products_list': vendor_products_list,
            'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
            'banner_top_left': Banners.objects.filter(position='Top Left'),
            'banner_top_middle': Banners.objects.filter(position='Top Middle'),
            'banner_top_right': Banners.objects.filter(position='Top Right'),
            'banner_middle_left': Banners.objects.filter(position='Middle Left'),
            'banner_middle_right': Banners.objects.filter(position='Middle Right'),
            'banner_down_left': Banners.objects.filter(position='Bottom Left'),
            'banner_down_middle': Banners.objects.filter(position='Bottom Middle'),
            'banner_down_right': Banners.objects.filter(position='Bottom Right'),
            'banner_collection': Banners.objects.filter(position='Collection Sidebar'),
            'category_banner': Banners.objects.filter(position='Categories Top'),
            'category_collection': Banners.objects.filter(position='Categories Sidebar'),
            'manufacture': Manufacturer.objects.filter(status='True'),

            ##############Category################
            'category_list': Categories.objects.all(),

            ####### products###########
            'product_list': product_list,  # New Products,
            'side_products': product_list[:3],  # New Products
            'side_products2': product_list[:3],  # New Products
            'new_products': product_list,  # New Products
            'new_products_updated': product_list,  # New Products Update
            'new_products_req': product_list,  # New Products add
            'new_featured': product_list,  # Featured Products
            'best_products': product_list,  # Best Sellers
            'categories_product': product_list,  # categories_product
            'products_related ': product_list,  # related_product
            'categories_side_products': product_list[:3],  # related_product
            'categories_side_products2': product_list[:3],  # related_product
            'category_side_products': product_list[:3],  # related_product
            'category_side_products2': product_list[:3],  # related_product
            'product_side_products': product_list[:3],  # related_product
            'product_side_products2': product_list[:3],  # related_product
            'related_product': product_list,  # related_product

            ##############Wishlist################

        }
    except BaseException as e:
        return {
                   'setting_data': None,
                   'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
                   'banner_left': Banners.objects.filter(media_location='left'),
                   'banner_right': Banners.objects.filter(title='right'),
                   'banner_down': Banners.objects.filter(title='down'),
                   'manufacture': Manufacturer.objects.filter(status='True'),
                   ####### products###########
                   'products_media': Products.objects.all(),  # New Products,
                   'side_products': product_list[:3],  # New Products
                   'side_products2': product_list[:3],  # New Products
                   'new_products': product_list,  # New Products
                   'new_products_updated': product_list,  # New Products Update
                   'new_products_req': product_list,  # New Products add
                   'new_featured': product_list,  # Featured Products
                   'best_products': product_list,  # Best Sellers
                   'categories_product': product_list,  # categories_product
                   'products_related ': product_list,  # related_product
                   'category_side_products': product_list[:3],  # related_product
                   'category_side_products2': product_list[:3],  # related_product
                   'product_side_products': product_list[:3],  # related_product
                   'product_side_products2': product_list[:3],  # related_product

               }, print(e);


def user_processors(request):
    if request.user.is_authenticated:

        user_address = UserAddress.objects.filter(user=request.user)
        return {
            'user_address': user_address,
            'wish_count': Wishlist.objects.filter(user=request.user).count()
        }
    else:
        return {
            'user_address': None,

        }


def filter_processors(request):
    category_p = Products.objects.distinct().values('category__title', 'category__id')
    brands_p= Products.objects.distinct().values('manufacturer__title', 'manufacturer__id')
    colors_p=Products.objects.distinct().values('variantdetails__color__name','variantdetails__color__id','variantdetails__color__code', )
    size_p=Products.objects.distinct().values('variantdetails__size__name','variantdetails__size__id','variantdetails__size__code',)
    minMaxPrice = Products.objects.aggregate(Min('price'), Max('price'))
    data={
        'category_p':category_p,
        'brands_p':brands_p,
        'colors_p':colors_p,
        'size_p':size_p,
        'minMaxPrice': minMaxPrice,

    }
    return data
