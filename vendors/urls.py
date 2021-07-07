from django import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path

from vendors.tests import CreateStoreTest
from vendors.views import store_list, edit_store, store_delete, \
    vendor_dashboard, SellerRegister, CreateStore,  CreateSuccess, StoreWaiting

app_name = 'vendors'


urlpatterns = [
    #path('v/login/',SellerLoginView.as_view(),name='seller_login'),
    #path('v/register/',SellerRegisterView.as_view(),name='seller_register'),

    ###############Adminn Seller Url##############
    path('admin/vendors/',store_list,name='store_list'),
    #path('admin/s/<int:id>',admin_dashboard,name='store_page'),
    path('admin/s/edit/', edit_store, name='edit_store'),
    path('admin/s/<int:id>', store_delete, name='store_delete'),



    ###############Front Seller Url##############
    path('register/seller/', SellerRegister.as_view(), name='SellerRegister'),
    path('startselling/',CreateStore.as_view(),name='CreateStore'),
    path('CreateSuccess/',CreateSuccess,name='CreateSuccess'),
    path('StoreWaiting/',StoreWaiting,name='StoreWaiting'),
    path('store/',vendor_dashboard,name='VendorDashboard'),







]