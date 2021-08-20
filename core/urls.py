from django.urls import path

from core.tests import AddSetting, UpdateSetting
from core.views.catalog import AddCategory, categories, EditCategory, DeleteCategory, \
    ProductsAddMedia, ProductEditMedia, ProductMediaDelete, ProductsAddStocks, file_upload, AdminIndex, \
    ProductsDeleted, DeleteManufacture, EditManufacture, AddManufacture, ManufacturerListView, \
    DeleteFilter, AddFilter, EditFilter, DeleteFiltersGroup, AddFiltersGroup, EditFiltersGroup, FiltersGroupListView, \
    FiltersListView, AttributesGroupListView, EditAttributesGroup, AddAttributesGroup, DeleteAttributesGroup, \
    AttributeListView, EditAttribute, AddAttribute, DeleteAttribute, ProductUpdate, ProductAdd, ProductsList,  \
    ManufacturerDetail, OptionsTypeListView, AddOptionsType, EditOptionsType, DeleteOptionsType, \
    OptionsListView, EditOption, AddOption, DeleteOption, \
    ColorListView, AddColor, EditColor, DeleteColor, SizeListView, EditSize, AddSize, DeleteSize, \
    VariantListView, load_option
from core.views.design import BannerDetailView, BannerDelete, \
    SliderView, SliderDelete, SliderGroupCreate, SliderDetailView, BannersView, BannerCreate, \
    SliderCreate
from core.views.order import OrdersListView, EditOrder, OrderDetailView
from core.views.setting import SettingDelete, AdminSetting
from core.views.users import AdminLogin, AdminLogout, AdminUserCreate, \
    AdminUserDetail, AdminUserEdit, AdminUserDelete, AdminUsersList

app_name = 'core'
"""
required(
    partial(login_required, admin_required, login_url='/accounts/login/'),
    (path('admin/', index, name='admin_index'),
"""

urlpatterns = [

    path('admin/', AdminIndex, name='AdminIndex'),

    # path('admin/logout', AdminIndex, name='AdminIndex'),


    ########## categories  #########
    path('admin/category/', categories, name='categories'),
    path('admin/category/edit/<int:pk>/', EditCategory.as_view(), name='EditCategory'),
    path('admin/category/add/', AddCategory, name='AddCategory'),
    path('admin/category/delete/<int:pk>/', DeleteCategory.as_view(), name='DeleteCategory'),

    ########## Products   #########
    # Products

    path('admin/products/', ProductsList.as_view(), name="ProductsList"),
    path('admin/products/ProductAdd', ProductAdd, name="ProductAdd"),
    path('admin/products/Product_edit/<str:product_id>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('admin/products/Products_delete/<int:pk>/', ProductsDeleted.as_view(), name="ProductDelete"),
    path('admin/products/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(), name="Products_add_media"),
    path('admin/products/Products_edit_media/<str:Products_id>', ProductEditMedia.as_view(),
         name="Products_edit_media"),
    path('admin/products/Products_media_delete/<str:id>', ProductMediaDelete.as_view(), name="Products_media_delete"),
    path('admin/products/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(),
         name="Products_add_stocks"),
    path('admin/products/file_upload', file_upload, name="file_upload"),

    ########## Filters  #########
    path('admin/FiltersGroup/', FiltersGroupListView.as_view(), name='FiltersGroup'),
    path('admin/FiltersGroup/edit/<int:pk>/', EditFiltersGroup.as_view(), name='EditFiltersGroup'),
    path('admin/FiltersGroup/add/', AddFiltersGroup.as_view(), name='AddFiltersGroup'),
    path('admin/FiltersGroup/delete/<int:pk>/', DeleteFiltersGroup.as_view(), name='DeleteFiltersGroup'),
    path('admin/Filters/', FiltersListView.as_view(), name='Filters'),
    path('admin/Filter/edit/<int:pk>/', EditFilter.as_view(), name='EditFilter'),
    path('admin/Filter/add/', AddFilter.as_view(), name='AddFilter'),
    path('admin/Filter/delete/<int:pk>/', DeleteFilter.as_view(), name='DeleteFilter'),

    ########## Attributes  #########
    path('admin/AttributesGroup/', AttributesGroupListView.as_view(), name='AttributesGroup'),
    path('admin/AttributesGroup/edit/<int:pk>/', EditAttributesGroup.as_view(), name='EditAttributesGroup'),
    path('admin/AttributesGroup/add/', AddAttributesGroup.as_view(), name='AddAttributesGroup'),
    path('admin/AttributesGroup/delete/<int:pk>/', DeleteAttributesGroup.as_view(), name='DeleteAttributesGroup'),
    path('admin/Attributes/', AttributeListView.as_view(), name='Attributes'),
    path('admin/Attribute/edit/<int:pk>/', EditAttribute.as_view(), name='EditAttribute'),
    path('admin/Attribute/add/', AddAttribute.as_view(), name='AddAttribute'),
    path('admin/Attribute/delete/<int:pk>/', DeleteAttribute.as_view(), name='DeleteAttribute'),

    ########## options  #########
    path('admin/OptionsType/', OptionsTypeListView.as_view(), name='OptionsType'),
    path('admin/OptionsType/edit/<int:pk>/', EditOptionsType.as_view(), name='EditOptionsType'),
    path('admin/OptionsType/add/', AddOptionsType.as_view(), name='AddOptionsType'),
    path('admin/OptionsType/delete/<int:pk>/', DeleteOptionsType.as_view(), name='DeleteOptionsType'),
    path('admin/Option/', OptionsListView.as_view(), name='Options'),
    path('admin/Option/edit/<int:pk>/', EditOption.as_view(), name='EditOption'),
    path('admin/Option/add/', AddOption.as_view(), name='AddOption'),
    path('admin/Option/delete/<int:pk>/', DeleteOption.as_view(), name='DeleteOption'),
    path('ajax/load-options/', load_option, name='ajax_load_options'),

    ########## Variant #########
    path('admin/Variant/', VariantListView.as_view(), name='Variant'),
    path('admin/Color/', ColorListView.as_view(), name='Color'),
    path('admin/Color/edit/<int:pk>/', EditColor.as_view(), name='EditColor'),
    path('admin/Color/add/', AddColor, name='AddColor'),
    path('admin/Color/delete/<int:pk>/', DeleteColor.as_view(), name='DeleteColor'),

    path('admin/Size/', SizeListView.as_view(), name='Size'),
    path('admin/Size/edit/<int:pk>/', EditSize.as_view(), name='EditSize'),
    path('admin/Size/add/', AddSize, name='AddSize'),
    path('admin/Size/delete/<int:pk>/', DeleteSize.as_view(), name='DeleteSize'),



    ########## Manufacturer   #########
    path('admin/manufacture/', ManufacturerListView.as_view(), name='Manufacturers'),
    path('admin/manufacture/add/', AddManufacture.as_view(), name='AddManufacturer'),
    path('admin/manufacture/edit/<int:pk>/', EditManufacture.as_view(), name='EditManufacturer'),
    path('admin/manufacture/edit/<int:pk>/', ManufacturerDetail.as_view(), name='ManufacturerDetail'),
    path('admin/manufacture/delete/<int:pk>/', DeleteManufacture.as_view(), name='DeleteManufacture'),

    ########## Sales   #########
    path('admin/sales/', OrdersListView.as_view(), name='Orders'),
    path('admin/sales/edit/<int:pk>/', EditOrder.as_view(), name='EditOrder'),
    path('admin/sales/edit/<int:pk>/', OrderDetailView.as_view(), name='OrderDetail'),

    ########## Slider   #########
    path('admin/slider', SliderView.as_view(), name='SliderView'),
    path('admin/slider/<int:pk>/', SliderDetailView.as_view(), name='SliderDetailView'),
    path('admin/slider/group/', SliderGroupCreate.as_view(), name='SliderGroupCreate'),
    path('admin/slider/create/', SliderCreate.as_view(), name='SliderCreate'),
    path('admin/slider/delete//<int:pk>/', SliderDelete.as_view(), name='SliderDelete'),

    ########## Banners   #########
    path('admin/design', BannersView.as_view(), name='BannerView'),
    path('admin/design/<int:pk>/', BannerDetailView.as_view(), name='BannerDetailView'),
    path('admin/design/create/', BannerCreate, name='BannerCreate'),
    path('admin/design/delete/<int:pk>/', BannerDelete.as_view(), name='BannerDelete'),

    ################ Users ################
    path('login/', AdminLogin.as_view(), name='AdminLogin'),
    path('admin/logout/', AdminLogout, name='AdminLogout'),
    path('admin/users/', AdminUsersList.as_view(), name='AdminUsersList'),
    path('admin/users/create/', AdminUserCreate.as_view(), name='AdminUserCreate'),
    path('admin/users/profile/<int:pk>', AdminUserDetail.as_view(), name='AdminUserDetail'),
    path('admin/users/uprofile/<int:pk>/', AdminUserEdit.as_view(), name='AdminUserEdit'),
    path('admin/users/dprofile/<int:id>', AdminUserDelete.as_view(), name='AdminUserDelete'),

    ########## setting   #########
    path('admin/setting/', AdminSetting.as_view(), name='AdminSetting'),
    path('admin/setting/add', AddSetting, name='AdminSiteAddSetting'),
    path('admin/setting/update/<slug:slug>', UpdateSetting.as_view(), name='UpdateSetting'),
    path('admin/setting/delete/<slug:slug>/', SettingDelete.as_view(), name='SettingDelete'),
]
