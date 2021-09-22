from django.urls import path

from vendors.tets2 import ProductCreateTest3
from vendors.views.catalog import VendorIndex, ProductsList,  ProductsDeleted, file_upload, \
    ProductsAddStocks, ProductMediaDelete, ProductEditMedia, ProductsAddMedia, ProductUpdate, VendorProductAdd
from vendors.views.order import VendorOrdersListView, VendorEditOrder, VendorOrderDetailView
from vendors.views.views import SellerRegister, CreateSuccess, StoreWaiting, VendorDashboard, EditStore, \
    AlreadyUserSellerRegister, VendorCreate, AllVendor

app_name = 'vendors'

urlpatterns = [



    ###############Front Seller Url##############
    path('register/seller/', SellerRegister, name='SellerRegister'),
    path('register/sellers/<slug:slug>', AlreadyUserSellerRegister, name='AlreadyUserSellerRegister'),
    path('startselling/', VendorCreate.as_view(), name='CreateStore'),
    path('CreateSuccess/', CreateSuccess, name='CreateSuccess'),
    path('StoreWaiting/', StoreWaiting, name='StoreWaiting'),

    path('vendor/', AllVendor, name='AllVendor'),
    path('vendor/<slug:slug>', VendorDashboard.as_view(), name='VendorDashboard'),
    path('vendor/edit/<slug:slug>', EditStore.as_view(), name='EditStore'),

############## Back ######################

    ########## Products   #########
    path('vendor/dashboard/', VendorIndex, name='VendorIndex'),
    path('vendor/dashboard/products/', ProductsList.as_view(), name="ProductsList"),
    path('vendor/dashboard/productcreate', VendorProductAdd, name="ProductCreate"),
    path('vendor/dashboard/products/Product_edit/<str:product_id>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('vendor/dashboard/products/Products_delete/<int:pk>/', ProductsDeleted.as_view(), name="ProductDelete"),
    path('vendor/dashboard/products/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(), name="Products_add_media"),
    path('vendor/dashboard/products/Products_edit_media/<str:Products_id>', ProductEditMedia.as_view(),
         name="Products_edit_media"),
     path('vendor/dashboard/products/Products_media_delete/<str:id>', ProductMediaDelete.as_view(), name="Products_media_delete"),
    path('vendor/dashboard/products/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(),
         name="Products_add_stocks"),
    path('vendor/dashboard/products/file_upload', file_upload, name="file_upload"),


########## Sales   #########
    path('vendor/dashboard/sales/', VendorOrdersListView.as_view(), name='Order'),
    path('vendor/dashboard/sales/edit/<int:pk>/', VendorEditOrder.as_view(), name='EditOrder'),
    path('vendor/dashboard/sales/<int:pk>/', VendorOrderDetailView.as_view(), name='OrderDetail'),

]
