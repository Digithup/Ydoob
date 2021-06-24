from django.urls import path, re_path, reverse_lazy, include
from django.views.generic import RedirectView

from localization import views
from localization.templatetags import rosetta
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

urlpatterns += (
    re_path(
        r'^$',
        RedirectView.as_view(
            url=reverse_lazy('rosetta-file-list', kwargs={'po_filter': 'project'}),
            permanent=False,
        ),
        name='rosetta-old-home-redirect',
    ),
    re_path(
        r'^files/$',
        RedirectView.as_view(
            url=reverse_lazy('rosetta-file-list', kwargs={'po_filter': 'project'}),
            permanent=False,
        ),
        name='rosetta-file-list-redirect',
    ),
    re_path(
        r'^files/(?P<po_filter>[\w-]+)/$',
        views.TranslationFileListView.as_view(),
        name='rosetta-file-list',
    ),
    re_path(
        r'^files/(?P<po_filter>[\w-]+)/(?P<lang_id>[\w\-_\.]+)/(?P<idx>\d+)/$',
        views.TranslationFormView.as_view(),
        name='rosetta-form',
    ),
    re_path(
        r'^files/(?P<po_filter>[\w-]+)/(?P<lang_id>[\w\-_\.]+)/(?P<idx>\d+)/download/$',
        views.TranslationFileDownload.as_view(),
        name='rosetta-download-file',
    ),
    re_path(r'^translate/$', views.translate_text, name='rosetta.translate_text'),
)