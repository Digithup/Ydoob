from django.conf import settings

from core.models.setting import Setting
from localization.models import Language


def core_processors(request):
    try:
        return {

                'setting': Setting.objects.filter(status=True),
                'index_language': Language.objects.all()


        }
    except Exception as e:
        return {

            'setting': None,
                'index_language': None

                }
