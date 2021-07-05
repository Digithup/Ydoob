from catalog.models.models import Products, ProductMedia
from catalog.models.product_options import Manufacturer
from core.models.design import SliderMedia, Slider, Banners
from core.models.setting import Setting, SettingMedia, SettingLang
from core.views.setting import setting
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
            'setting_data': SettingLang.objects.get(lang='en'),
            'setting_data_ar': SettingLang.objects.get(lang='ar'),
            'index_language': Language.objects.all(),
            ####### products###########
            'products_media' : ProductMedia.objects.all() , # New Products,
            'new_products' : Products.objects.all() , # New Products
        }
    except Exception as e:
        return {'setting': Setting.objects.last(),
                'setting_media': SettingMedia.objects.last(),
                'main_slider': SliderMedia.objects.filter(slider_id__group__title='home'),
                'banner_left': Banners.objects.filter(media_location='left'),
                'banner_right': Banners.objects.filter(title='right'),
                'banner_down': Banners.objects.filter(title='down'),
                'manufacture': Manufacturer.objects.filter(status='True'),
                # 'banner': Banners.objects.all(),
                'setting_data': SettingLang.objects.get(lang='en'),
                'setting_data_ar': SettingLang.objects.get(lang='ar'),
                'index_language': Language.objects.all()

                }
