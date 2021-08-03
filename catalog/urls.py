from django.conf.urls import url
from django.urls import path, include


from catalog.views import views
from catalog.api import api
from catalog.views.views import FilterSearch

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='/index'),
    path('FilterSearch/',FilterSearch, name='FilterSearch'),
    # path('category/', views.category_list, name='category_list'),


   # path('category/<int:id>/<slug:slug>/', views.Products_detail, name='Products_detail'),

    # API
    path('api/category', api.category_list_api, name='category_list_api'),
    path('api/category/<int:id>', api.category_details_api, name='category_details_api'),
    path('admin/api/category', api.category_list_api, name='category_list_api'),

    # class based views

    path('api/v2/catalog/category', api.CategoryListAPi.as_view(), name='CategoryListAPi'),
    path('api/v2/catalog/category/<int:id>', api.CategoryApi.as_view(), name='CategoryAPi'),
    path('api/v2/catalog/products/', api.ProductsListApi.as_view(), name='ProductsListAPi'),
    path('api/v2/category/product/<int:id>', api.ProductsApi.as_view(), name='ProductsAPi'),


    #path('FilterAutocomplete/', FilterAutocomplete, name='FilterAutocomplete')



]



