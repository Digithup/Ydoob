from django.urls import path

from . import search, views
from .tests import product_detailtest
from .views import CategoriesDetail, CategoryDetail, ProductsListView, ProductSearch, error403, product_detail

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),

    ############ search ##############
    path('product/search', ProductSearch, name='search'),

    ############ Category Product ##############
    path('categories/', CategoriesDetail, name='Categories'),
    path('categories/<int:id>/<slug:slug>', CategoryDetail, name='Category'),
    path('products/', ProductsListView, name='ProductsView'),

    ############ Product ##############
    # path('product/<slug:slug>/', ProductDetailView.as_view(), name='ProductDetail'),
    path('product/<int:id>/<slug:slug>/', product_detail, name='ProductDetail'),

    # path('search/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),

    ############ Filter ##############
    # path('product/filter', FilterCategoryView.as_view(), name='FilterCategory'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('product/load-more-data', views.load_more_data, name='load_more_data'),



    ###############ErrorPage#############
path('403', error403, name='Error403'),


]
