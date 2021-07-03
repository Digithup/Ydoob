from django.urls import path

from core.tests import SettingAddViewTest
from core.views.design import BannerDetailView, BannerDelete, \
    SliderView, SliderDelete, SliderGroupCreate, SliderDetailView, BannersView, BannerCreate, \
    SliderCreate

from core.views.catalog import AddCategory, categories, EditCategory, DeleteCategory, ProductsListView, \
    ProductsEdit, ProductsAddMedia, ProductsEditMedia, ProductsMediaDelete, ProductsAddStocks, file_upload, index, \
    ProductAddView, ProductsDeleted, DeleteManufacture, EditManufacture, AddManufacture, ManufacturerListView
from core.views.setting import update_setting

app_name = 'core'
urlpatterns = [

    path('admin/', index, name='admin_index'),

    ########## categories  #########
    path('admin/category/', categories, name='categories'),
    # path('admin/category/edit/<int:pk>/', EditCategory, name='EditCategory'),
    path('admin/category/edit/<int:pk>/', EditCategory.as_view(), name='EditCategory'),
    path('admin/category/add/', AddCategory, name='AddCategory'),
    path('admin/category/delete/<int:pk>/', DeleteCategory.as_view(), name='delete_category'),

    ########## Products   #########
    # Products
    path('admin/products/Products_create', ProductAddView.as_view(), name="Product_add"),
    path('admin/products/Products_list', ProductsListView.as_view(), name="Products_list"),
    path('admin/products/Products_edit/<str:Products_id>', ProductsEdit.as_view(), name="ProductUpdate"),
    path('admin/products/Products_delete/<int:pk>/', ProductsDeleted.as_view(), name="Product_Delete"),
    path('admin/products/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(), name="Products_add_media"),
    path('admin/products/Products_edit_media/<str:Products_id>', ProductsEditMedia.as_view(), name="Products_edit_media"),
    path('admin/products/Products_media_delete/<str:id>', ProductsMediaDelete.as_view(), name="Products_media_delete"),
    path('admin/products/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(), name="Products_add_stocks"),
    path('admin/products/file_upload', file_upload, name="file_upload"),

    ########## options  #########
    # path('admin/options/', categories, name='options'),
    # path('admin/options/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditoOtions'),
    # path('admin/options/add/', AddCategory, name='AddOptions'),
    # path('admin/options/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_options'),

    ########## Manufacturer   #########
    # path('admin/Products/', views.Products_admin, name='Products_admin'),
    # path('admin/manufacture/', views.AddManufacturer, name='manufacture'),
    # path('admin/catalog/<int:pk>/', views.ProductsDetailView.as_view(), name='ProductsDetail'),
    # path('admin/catalog/edit/<int:pk>/<slug:slug>/', ProductsUpdate.as_view(), name='ProductsUpdate'),
    # path('admin/catalog/create/', ProductsCreate.as_view(), name='ProductsCreate'),
    # path('admin/catalog/create/', addProductsView, name='addProductsView'),
    # path('admin/catalog/delete/<int:id>/<slug:slug>/', ProductsDelete.as_view(), name='ProductsDelete'),

    # path('admin/catalog/', ProductsView.as_view(), name='ProductsView'),
    # path('admin/catalog/create/', ProductsCreateView.as_view(), name='ProductsCreateView'),
    # path('admin/catalog/<int:pk>/', ProductsDetailView.as_view(), name='ProductsDetailView'),

    ########## Manufacturer   #########
    path('admin/manufacture/', ManufacturerListView.as_view(), name='Manufacturers'),
    path('admin/manufacture/edit/<int:pk>/', EditManufacture.as_view(), name='EditManufacturer'),
    path('admin/manufacture/add/', AddManufacture.as_view(), name='AddManufacturer'),
    path('admin/manufacture/delete/<int:pk>/', DeleteManufacture.as_view(), name='DeleteManufacture'),

    ########## Slider   #########
    path('admin/slider', SliderView.as_view(), name='SliderView'),
    path('admin/slider/<int:pk>/', SliderDetailView.as_view(), name='SliderDetailView'),
    path('admin/slider/group/', SliderGroupCreate.as_view(), name='SliderGroupCreate'),
    path('admin/slider/create/', SliderCreate.as_view(), name='SliderCreate'),
    path('admin/slider/delete//<int:pk>/', SliderDelete.as_view(), name='SliderDelete'),

    ########## Banners   #########
    path('admin/banner', BannersView.as_view(), name='BannerView'),
    path('admin/banner/<int:pk>/', BannerDetailView.as_view(), name='BannerDetailView'),
    path('admin/banner/create/', BannerCreate.as_view(), name='BannerCreate'),
    path('admin/banner/delete//<int:pk>/', BannerDelete.as_view(), name='BannerDelete'),





########## setting   #########
    # path('admin/setting/add/', SettingAddViewTest.as_view(), name='add_setting'),
    path('admin/setting/add/', SettingAddViewTest.as_view(), name='add_setting'),
    path('admin/setting/', update_setting, name='update_setting'),

]
