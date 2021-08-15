from django.urls import path
from . import views
from .views import ProductDetailView, autocomplete, CategoriesDetail, CategoryDetail, ProductsListView, ajaxcolor, \
    product_detail

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('search/autocomplete', autocomplete, name='autocomplete'),
path('ajaxcolor/', ajaxcolor, name='ajaxcolor'),
    # path('search/', SearchView(), name='search'),
    # path('search_auto/', views.search_auto, name='search_auto'),

    ############ Category Product ##############
    path('categories/', CategoriesDetail, name='Categories'),
    path('categories/<slug:slug>', CategoryDetail.as_view(), name='Category'),
    path('products/', ProductsListView.as_view(), name='ProductsView'),

    ############ Product ##############
    #path('product/<slug:slug>/', ProductDetailView.as_view(), name='ProductDetail'),
    path('product/<slug:slug>/', product_detail, name='ProductDetail'),
    #path('search/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),

]
product_detail