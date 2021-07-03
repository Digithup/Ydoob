from django.urls import path, include

from . import views
from .views import ProductDetailView, autocomplete, ProductsHomeListView, categories

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('search/autocomplete', autocomplete, name='autocomplete'),
    #path('search/', SearchView(), name='search'),

    #path('search_auto/', views.search_auto, name='search_auto'),

    ############ Category Product ##############
    path('categories/', categories, name='CategoriesView'),
    path('products/', ProductsHomeListView.as_view(), name='ProductsView'),


    ############ Product ##############
    path('product/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),
    #path('search/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),

]