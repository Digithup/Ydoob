from django.conf import settings

from core.models.setting import Setting, SettingLang
from localization.models import Language


def core_processors(request):
    try:
        return {

                'setting': Setting.objects.filter(status=True),



        }
    except Exception as e:
        return {

            'setting': None,


                }
