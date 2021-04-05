from django.urls import path

from localization import views
from localization.views import all_lang, AddLang, EditLang, DeleteLang, ActivateLanguageView

app_name = 'localization'
urlpatterns = [

    path('language/activate/<language_code>/', ActivateLanguageView.as_view(), name='activate_language'),
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    # path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),

    ########## categories  #########
    path('admin/lang/', all_lang, name='all_lang'),
    path('admin/lang/edit/<pk>/', EditLang.as_view(), name='EditLang'),
    path('admin/lang/add/', AddLang.as_view(), name='AddLang'),
    path('admin/lang/delete/<pk>/', DeleteLang.as_view(), name='DeleteLang'),
]
