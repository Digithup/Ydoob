from core.models.design import SliderMedia, Slider
from core.models.setting import Setting,  SettingLang
from core.views.setting import setting
from localization.models import Language


def core_processors(request):
    try:
        return {

                'setting': Setting.objects.filter(status=True),
                'index_language': Language.objects.all()


        }
    except Exception as e:
        return {'setting': Setting.objects.last(),
                'index_language': Language.objects.all()

                }
