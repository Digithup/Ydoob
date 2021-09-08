"""DNigne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import notification
from home.tests import ajaxcolortest,  ajaxpricetest
from localization import views


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    # path('savelangcur', views.savelangcur, name='savelangcur'),

]

urlpatterns += i18n_patterns(
    url(r'^oauth/', include('social_django.urls', namespace='social')),
     path('currencies/', include('currencies.urls')),
    path('admin/', admin.site.urls),
    path('', include('user.urls'), name='user'),
    path('dashboard/', include('core.urls'), name='core'),
    path('', include('localization.urls'), name='localization'),
    path('', include('notification.urls'),name='notifications'),
    path('', include('home.urls'), name='home'),
    path('', include('catalog.urls'), name='catalog'),
    path('', include('sales.urls'), name='sales'),
    path('', include('vendors.urls'), name='vendors'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('ajaxcolor/', ajaxcolortest, name='ajaxcolor'),
    path('ajaxprice/', ajaxpricetest, name='ajaxprice'),


    # path('search/', SearchView(), name='search'),
    # path('search_auto/', search_auto, name='search_auto'),



    # prefix_default_language=True,

)

# handler404 = error.error_handler
# handler500 = error.error_handler
# ... the rest of your URLconf goes here ...
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/lang/rosetta/', include('rosetta.urls'))
    ]
