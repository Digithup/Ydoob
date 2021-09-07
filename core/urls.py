from django.urls import path, include
from django.urls import path
import notifications.urls
from core.tests import AddSetting, UpdateSetting
from core.views.catalog import AddCategory, categories, EditCategory, DeleteCategory, \
    ProductsAddMedia, ProductEditMedia, ProductMediaDelete, ProductsAddStocks, file_upload, AdminIndex, \
    ProductsDeleted, DeleteManufacture, EditManufacture, AddManufacture, ManufacturerListView, \
    DeleteFilter, AddFilter, EditFilter, DeleteFiltersGroup, AddFiltersGroup, EditFiltersGroup, FiltersGroupListView, \
    FiltersListView, AttributesGroupListView, EditAttributesGroup, AddAttributesGroup, DeleteAttributesGroup, \
    AttributeListView, EditAttribute, AddAttribute, DeleteAttribute, ProductUpdate, ProductAdd, ProductsList, \
    ManufacturerDetail, OptionsTypeListView, AddOptionsType, EditOptionsType, DeleteOptionsType, \
    OptionsListView, EditOption, AddOption, DeleteOption, \
    ColorListView, AddColor, EditColor, DeleteColor, SizeListView, EditSize, AddSize, DeleteSize, \
    VariantListView, load_option
from core.views.design import BannerDetailView, BannerDelete, \
    SliderView, SliderDelete, SliderGroupCreate, SliderDetailView, BannersView, BannerCreate, \
    SliderCreate
from core.views.order import OrdersListView, EditOrder, OrderDetailView
from core.views.setting import SettingDelete, AdminSetting, AdminSite, AdminSiteUpdate, PaymentMethodsList, \
    PaymentMethodsDelete, PaymentMethodsUpdate, PaymentMethodsCreate
from core.views.users import AdminLogin, AdminLogout, AdminUserCreate, \
    AdminUserDetail, AdminUserEdit, AdminUserDelete, AdminUsersList, AdminUserGroupList, AdminUserGroupCreate, \
    AdminUserGroupDelete, AdminUserGroupEdit

app_name = 'core'

urlpatterns = [

    path('', AdminIndex, name='AdminIndex'),

    # path('admin/logout', AdminIndex, name='AdminIndex'),

    ########## categories  #########
    path('category/', categories, name='categories'),
    path('category/edit/<int:pk>/', EditCategory.as_view(), name='EditCategory'),
    path('category/add/', AddCategory, name='AddCategory'),
    path('category/delete/<int:pk>/', DeleteCategory.as_view(), name='DeleteCategory'),

    ########## Products   #########
    # Products

    path('products/', ProductsList.as_view(), name="ProductsList"),
    path('products/ProductAdd', ProductAdd, name="ProductAdd"),
    path('products/Product_edit/<str:product_id>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('products/Products_delete/<int:pk>/', ProductsDeleted.as_view(), name="ProductDelete"),
    path('products/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(),
         name="Products_add_media"),
    path('products/Products_edit_media/<str:Products_id>', ProductEditMedia.as_view(),
         name="Products_edit_media"),
    path('products/Products_media_delete/<str:id>', ProductMediaDelete.as_view(),
         name="Products_media_delete"),
    path('products/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(),
         name="Products_add_stocks"),
    path('products/file_upload', file_upload, name="file_upload"),

    ########## Filters  #########
    path('FiltersGroup/', FiltersGroupListView.as_view(), name='FiltersGroup'),
    path('FiltersGroup/edit/<int:pk>/', EditFiltersGroup.as_view(), name='EditFiltersGroup'),
    path('FiltersGroup/add/', AddFiltersGroup.as_view(), name='AddFiltersGroup'),
    path('FiltersGroup/delete/<int:pk>/', DeleteFiltersGroup.as_view(), name='DeleteFiltersGroup'),
    path('Filters/', FiltersListView.as_view(), name='Filters'),
    path('Filter/edit/<int:pk>/', EditFilter.as_view(), name='EditFilter'),
    path('Filter/add/', AddFilter.as_view(), name='AddFilter'),
    path('Filter/delete/<int:pk>/', DeleteFilter.as_view(), name='DeleteFilter'),

    ########## Attributes  #########
    path('AttributesGroup/', AttributesGroupListView.as_view(), name='AttributesGroup'),
    path('AttributesGroup/edit/<int:pk>/', EditAttributesGroup.as_view(), name='EditAttributesGroup'),
    path('AttributesGroup/add/', AddAttributesGroup.as_view(), name='AddAttributesGroup'),
    path('AttributesGroup/delete/<int:pk>/', DeleteAttributesGroup.as_view(), name='DeleteAttributesGroup'),
    path('Attributes/', AttributeListView.as_view(), name='Attributes'),
    path('Attribute/edit/<int:pk>/', EditAttribute.as_view(), name='EditAttribute'),
    path('Attribute/add/', AddAttribute.as_view(), name='AddAttribute'),
    path('Attribute/delete/<int:pk>/', DeleteAttribute.as_view(), name='DeleteAttribute'),

    ########## options  #########
    path('OptionsType/', OptionsTypeListView.as_view(), name='OptionsType'),
    path('OptionsType/edit/<int:pk>/', EditOptionsType.as_view(), name='EditOptionsType'),
    path('OptionsType/add/', AddOptionsType.as_view(), name='AddOptionsType'),
    path('OptionsType/delete/<int:pk>/', DeleteOptionsType.as_view(), name='DeleteOptionsType'),
    path('Option/', OptionsListView.as_view(), name='Options'),
    path('Option/edit/<int:pk>/', EditOption.as_view(), name='EditOption'),
    path('Option/add/', AddOption.as_view(), name='AddOption'),
    path('Option/delete/<int:pk>/', DeleteOption.as_view(), name='DeleteOption'),
    path('ajax/load-options/', load_option, name='ajax_load_options'),

    ########## Variant #########
    path('Variant/', VariantListView.as_view(), name='Variant'),
    path('Color/', ColorListView.as_view(), name='Color'),
    path('Color/edit/<int:pk>/', EditColor.as_view(), name='EditColor'),
    path('Color/add/', AddColor, name='AddColor'),
    path('Color/delete/<int:pk>/', DeleteColor.as_view(), name='DeleteColor'),

    path('Size/', SizeListView.as_view(), name='Size'),
    path('Size/edit/<int:pk>/', EditSize.as_view(), name='EditSize'),
    path('Size/add/', AddSize, name='AddSize'),
    path('Size/delete/<int:pk>/', DeleteSize.as_view(), name='DeleteSize'),

    ########## Manufacturer   #########
    path('manufacture/', ManufacturerListView.as_view(), name='Manufacturers'),
    path('manufacture/add/', AddManufacture.as_view(), name='AddManufacturer'),
    path('manufacture/edit/<int:pk>/', EditManufacture.as_view(), name='EditManufacturer'),
    path('manufacture/edit/<int:pk>/', ManufacturerDetail.as_view(), name='ManufacturerDetail'),
    path('manufacture/delete/<int:pk>/', DeleteManufacture.as_view(), name='DeleteManufacture'),

    ########## Sales   #########
    path('sales/', OrdersListView.as_view(), name='Order'),
    path('sales/edit/<int:pk>/', EditOrder.as_view(), name='EditOrder'),
    path('sales/<int:pk>/', OrderDetailView.as_view(), name='OrderDetail'),

    ########## Slider   #########
    path('slider', SliderView.as_view(), name='SliderView'),
    path('slider/<int:pk>/', SliderDetailView.as_view(), name='SliderDetailView'),
    path('slider/groups/', SliderGroupCreate.as_view(), name='SliderGroupCreate'),
    path('slider/create/', SliderCreate.as_view(), name='SliderCreate'),
    path('slider/delete//<int:pk>/', SliderDelete.as_view(), name='SliderDelete'),

    ########## Banners   #########
    path('design', BannersView.as_view(), name='BannerView'),
    path('design/<int:pk>/', BannerDetailView.as_view(), name='BannerDetailView'),
    path('design/create/', BannerCreate, name='BannerCreate'),
    path('design/delete/<int:pk>/', BannerDelete.as_view(), name='BannerDelete'),

    ################ Users ################
    path('login/', AdminLogin.as_view(), name='AdminLogin'),
    path('logout/', AdminLogout, name='AdminLogout'),

    path('Users/', AdminUsersList.as_view(), name='AdminUsersList'),
    path('Users/create/', AdminUserCreate.as_view(), name='AdminUserCreate'),
    path('Users/profile/<int:pk>', AdminUserDetail.as_view(), name='AdminUserDetail'),
    path('Users/uprofile/<int:pk>/', AdminUserEdit.as_view(), name='AdminUserEdit'),
    path('Users/dprofile/<int:id>', AdminUserDelete.as_view(), name='AdminUserDelete'),

    path('groups/', AdminUserGroupList.as_view(), name='AdminUserGroupList'),
    path('groups/create/', AdminUserGroupCreate.as_view(), name='AdminUserGroupCreate'),
    path('groups/edit/<int:pk>', AdminUserGroupEdit.as_view(), name='AdminUserGroupEdit'),
    path('groups/delete/<int:id>', AdminUserGroupDelete.as_view(), name='AdminUserGroupDelete'),

    ########## setting   #########
    path('setting/', AdminSetting.as_view(), name='AdminSetting'),
    path('setting/add', AddSetting, name='AdminSiteAddSetting'),
    path('setting/update/<slug:slug>', UpdateSetting.as_view(), name='UpdateSetting'),
    path('setting/delete/<slug:slug>/', SettingDelete.as_view(), name='SettingDelete'),

    path('setting/payment/', PaymentMethodsList.as_view(), name='PaymentMethodsList'),
    path('setting/payment', PaymentMethodsCreate.as_view(), name='PaymentMethodsCreate'),
    path('setting/payment/update/<slug:slug>', PaymentMethodsUpdate.as_view(), name='PaymentMethodsUpdate'),
    path('setting/payment/delete/<slug:slug>/', PaymentMethodsDelete.as_view(), name='PaymentMethodsDelete'),

    path('site/', AdminSite.as_view(), name='AdminSite'),
    path('site/update/<int:pk>', AdminSiteUpdate.as_view(), name='AdminSiteUpdate'),


path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
