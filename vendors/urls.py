from django.urls import path

from vendors.tets2 import ProductCreateTest3
from vendors.views.catalog import VendorIndex, ProductsList, ProductCreate, ProductsDeleted, file_upload, \
    ProductsAddStocks, ProductMediaDelete, ProductEditMedia, ProductsAddMedia, ProductUpdate
from vendors.views.views import SellerRegister, CreateStore, CreateSuccess, StoreWaiting, VendorDashboard, EditStore

app_name = 'vendors'

urlpatterns = [



    ###############Front Seller Url##############
    path('register/seller/', SellerRegister.as_view(), name='SellerRegister'),
    path('startselling/', CreateStore.as_view(), name='CreateStore'),
    path('CreateSuccess/', CreateSuccess, name='CreateSuccess'),
    path('StoreWaiting/', StoreWaiting, name='StoreWaiting'),
    path('store/<str:store_id>', VendorDashboard.as_view(), name='VendorDashboard'),
    path('store/edit/<str:store_id>', EditStore.as_view(), name='EditStore'),

############## Back ######################

    ########## Products   #########
    path('store/dashboard/', VendorIndex, name='VendorIndex'),
    path('store/dashboard/products/', ProductsList.as_view(), name="ProductsList"),
    path('store/dashboard/productcreate', ProductCreateTest3.as_view(), name="ProductCreate"),

    path('store/dashboard/products/Product_edit/<str:product_id>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('store/dashboard/products/Products_delete/<int:pk>/', ProductsDeleted.as_view(), name="Product_Delete"),
    path('store/dashboard/products/Products_add_media/<str:Products_id>', ProductsAddMedia.as_view(), name="Products_add_media"),
    path('store/dashboard/products/Products_edit_media/<str:Products_id>', ProductEditMedia.as_view(),
         name="Products_edit_media"),
     path('store/dashboard/products/Products_media_delete/<str:id>', ProductMediaDelete.as_view(), name="Products_media_delete"),
    path('store/dashboard/products/Products_add_stocks/<str:Products_id>', ProductsAddStocks.as_view(),
         name="Products_add_stocks"),
    path('store/dashboard/products/file_upload', file_upload, name="file_upload"),

]
