from django.conf.urls import url
from django.urls import path

from .views.address import DeleteAddress, UpdateAddress, CreateAddress, address_list
from .views.users import customer_logout, CustomerRegister, CustomerLogin
from .views.views import guest_user_view, UserProfile, UpdateProfile, UpdateImage

app_name = 'user'

urlpatterns = [

    path('guest-user/', guest_user_view, name='guest_user_register'),

    ##########Customer################

    path('login/', CustomerLogin.as_view(), name='CustomerLogin'),
    path('register/', CustomerRegister.as_view(), name='CustomerRegister'),
    path('logout/', customer_logout, name='CustomerLogout'),

    path('user/profile/<slug:slug>', UserProfile, name='UserProfile'),
    path('user/uproile/<slug:slug>', UpdateImage, name='UpdateImage'),
    path('user/uprofile/<slug:slug>', UpdateProfile, name='UpdateProfile'),

    ##########Address################
    path('user/booklist/', address_list, name='address_list'),
    # path('user/cadress/', address_create, name='CreateAddress'),
    path('user/cadress/', CreateAddress, name='CreateAddress'),
    # path('user/uadress/<int:pk>', UpdateAddress, name='UpdateAddress'),
    path('user/adress/<int:pk>', DeleteAddress, name='DeleteAddress'),
    url(r'^user/adress/(?P<pk>\d+)/update/$', UpdateAddress, name='UpdateAddress'),
    # path('admin/create-profile',AddProfile.as_view(),name='create_profile'),
    # path('guest-user/',guest_user_view,name='guest_user_register'),
    # path('users/', UsersView.as_view(), name='UserList'),
    # path('create-user/', UserAdminCreationForm, name='CreateUser'),

    ##########Seller################

    # path('users/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup')
    # path('register/seller/',SellerRegister.as_view(),name='SellerRegister'),
]
