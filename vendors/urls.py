from django.urls import path

from vendors.tests import EditStoreTest
from vendors.views import SellerRegister, CreateStore, CreateSuccess, StoreWaiting, VendorDashboard

app_name = 'vendors'


urlpatterns = [
    #path('v/login/',SellerLoginView.as_view(),name='seller_login'),
    #path('v/register/',SellerRegisterView.as_view(),name='seller_register'),

    ###############Adminn Seller Url##############
    #path('admin/vendors/',store_list,name='store_list'),
    #path('admin/s/<int:id>',admin_dashboard,name='store_page'),
    #path('admin/s/edit/', EditStore, name='EditStore'),
    #path('admin/s/<int:id>', store_delete, name='store_delete'),



    ###############Front Seller Url##############
    path('register/seller/', SellerRegister.as_view(), name='SellerRegister'),
    path('startselling/',CreateStore.as_view(),name='CreateStore'),
    path('CreateSuccess/',CreateSuccess,name='CreateSuccess'),
    path('StoreWaiting/',StoreWaiting,name='StoreWaiting'),
    path('store/<int:vendor>',VendorDashboard.as_view(),name='VendorDashboard'),
    path('store/edit/<str:store_id>', EditStoreTest.as_view(), name='EditStore'),







]