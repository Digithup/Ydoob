from django import views
from django.urls import path

from core.tests import banner_create
from core.views.banners_views import BannerView, BannerDetailView, BannerDelete

from core.views.setting_views import update_setting, add_setting
from core.views.views import AddCategory, categories, EditCategory, DeleteCategory, ProductsListView, \
    ProductsEdit, ProductsAddMedia, ProductsEditMedia, ProductsMediaDelete, ProductsAddStocks, file_upload, index, \
    AddProductView, ProductView, EditCategoryz

app_name = 'core'
urlpatterns = [

    path('admin/', index, name='admin_index'),

    ########## categories  #########
    path('admin/category/', categories, name='categories'),
    #path('admin/category/edit/<int:pk>/', EditCategory, name='EditCategory'),
    path('admin/category/edit/<int:pk>/', EditCategoryz.as_view(), name='EditCategory'),
    path('admin/category/add/', AddCategory, name='AddCategory'),
    path('admin/category/delete/<int:pk>/', DeleteCategory.as_view(), name='delete_category'),

    ########## Products   #########
    # Products
    path('admin/Products_create', ProductView.as_view(), name="Products_view"),
    path('admin/Products_list', ProductsListView.as_view(), name="Products_list"),
    path('admin/Products_edit/<str:Products_id>', ProductsEdit.as_view(), name="Products_edit"),
    path('admin/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(), name="Products_add_media"),
    path('admin/Products_edit_media/<str:Products_id>', ProductsEditMedia.as_view(), name="Products_edit_media"),
    path('admin/Products_media_delete/<str:id>', ProductsMediaDelete.as_view(), name="Products_media_delete"),
    path('admin/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(), name="Products_add_stocks"),
    path('admn/file_upload',file_upload,name="file_upload"),

    ########## options  #########
    #path('admin/options/', categories, name='options'),
    #path('admin/options/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditoOtions'),
    #path('admin/options/add/', AddCategory, name='AddOptions'),
    #path('admin/options/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_options'),

    ########## Manufacturer   #########
    # path('admin/Products/', views.Products_admin, name='Products_admin'),
    # path('admin/manufacturer/', views.AddManufacturer, name='manufacturer'),
    # path('admin/catalog/<int:pk>/', views.ProductsDetailView.as_view(), name='ProductsDetail'),
    # path('admin/catalog/edit/<int:pk>/<slug:slug>/', ProductsUpdate.as_view(), name='ProductsUpdate'),
    # path('admin/catalog/create/', ProductsCreate.as_view(), name='ProductsCreate'),
    # path('admin/catalog/create/', addProductsView, name='addProductsView'),
    # path('admin/catalog/delete/<int:id>/<slug:slug>/', ProductsDelete.as_view(), name='ProductsDelete'),

    # path('admin/catalog/', ProductsView.as_view(), name='ProductsView'),
    # path('admin/catalog/create/', ProductsCreateView.as_view(), name='ProductsCreateView'),
    # path('admin/catalog/<int:pk>/', ProductsDetailView.as_view(), name='ProductsDetailView'),

    ########## Manufacturer   #########
    path('admin/setting/', update_setting, name='update_setting'),
    path('admin/setting/add/', add_setting, name='add_setting'),

    ########## Banners   #########
    path('admin/banner', BannerView.as_view(), name='BannerView'),
    path('admin/banner/<int:pk>/', BannerDetailView.as_view(), name='BannerDetailView'),
    path('admin/banner/create/', banner_create, name='add_banner'),
    path('admin/banner/delete//<int:pk>/', BannerDelete.as_view(), name='BannerDelete'),

]
