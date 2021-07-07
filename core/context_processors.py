from core.models.design import SliderMedia, Slider
from core.models.setting import Setting, SettingMedia, SettingLang
from core.views.setting import setting
from localization.models import Language


def core_processors(request):
    try:
        return {
                'setting_data': SettingLang.objects.all(),
                'setting': Setting.objects.last(),
                'setting_media': SettingMedia.objects.last(),
                'index_language': Language.objects.all()


        }
    except Exception as e:
        return {'setting': Setting.objects.last(),
                'setting_media': SettingMedia.objects.last(),
                'index_language': Language.objects.all()

                }
