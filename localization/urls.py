from django.urls import path

from localization import views
from localization.views import all_lang, AddLang, EditLang, DeleteLang

app_name = 'localization'
urlpatterns = [


    ########## categories  #########
    path('admin/lang/', all_lang, name='all_lang'),
    path('admin/lang/edit/<pk>/', EditLang, name='EditLang'),
    path('admin/lang/add/', AddLang.as_view(), name='AddLang'),
    path('admin/lang/delete/<pk>/', DeleteLang, name='DeleteLang'),
]
