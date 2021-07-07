from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView

from localization import views
from localization.views import all_lang, AddLang, EditLang, DeleteLang

app_name = 'localization'
urlpatterns = [


    ########## categories  #########
    path('admin/lang/', all_lang, name='all_lang'),
    path('admin/lang/edit/<pk>', EditLang.as_view(), name='EditLang'),
    path('admin/lang/add/', AddLang.as_view(), name='AddLang'),
    path('admin/lang/delete/<pk>/', DeleteLang.as_view(), name='DeleteLang'),



    #path('admin/lang/rosetta/<po_filter>/(?P<lang_id>[\w\-_\.]+)/(?P<idx>\d+)/', views.TranslationFormView.as_view() , name='EditTranslation')


#############Rosetta##########

]

