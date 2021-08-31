from django.conf import settings

from core.models.setting import Setting, SettingLang
from localization.models import Language


def core_processors(request):
    try:
        return {

                'setting': Setting.objects.filter(status=True),
            'setting_lang': SettingLang.objects.all(),
                'index_language': Language.objects.all()


        }
    except Exception as e:
        return {

            'setting': None,
            'setting_lang':None,
            'index_language': None

                }
