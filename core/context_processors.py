from core.models.models import Setting
from core.views.setting_views import setting
from localization.models import Language


def site_profile(request):
    return {'setting': Setting.objects.first(),
            'index_language':Language.objects.all()

            }
