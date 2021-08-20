from django.urls import path

from . import views
from .search import SearchView
from .tests import product_detailtest
from .views import  CategoriesDetail, CategoryDetail, ProductsListView, product_detail

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),


############ search ##############



    ############ Category Product ##############
    path('categories/', CategoriesDetail, name='Categories'),
    path('categories/<int:id>/<slug:slug>', CategoryDetail, name='Category'),
    path('products/', ProductsListView.as_view(), name='ProductsView'),

    ############ Product ##############
    #path('product/<slug:slug>/', ProductDetailView.as_view(), name='ProductDetail'),
    path('product/<int:id>/<slug:slug>/', product_detailtest, name='ProductDetail'),

    #path('search/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),

]
product_detail