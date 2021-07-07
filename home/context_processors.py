from catalog.models.models import Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Banners
from core.models.setting import Setting, SettingMedia, SettingLang

from localization.models import Language


def home_processors(request):
    try:
        return {
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
            'products_media' : ProductMedia.objects.all() , # New Products,
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


                },print(e);

