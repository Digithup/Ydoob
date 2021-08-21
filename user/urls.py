from django.conf.urls import url
from django.urls import path
from django.contrib.auth import  views as auth_views
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


    ###########Password###########
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),


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
