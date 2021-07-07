
from django.urls import path

from .views.users import customer_logout, CustomerRegister, CustomerLogin
from .views.views import guest_user_view

app_name = 'user'


urlpatterns = [


    path('guest-user/',guest_user_view,name='guest_user_register'),

    ##########Customer################

    path('login/',CustomerLogin.as_view(),name='CustomerLogin'),
    path('register/',CustomerRegister.as_view(),name='CustomerRegister'),
    path('logout/',customer_logout,name='CustomerLogout'),

    #path('user/profile',profile,name='customer_profile'),
    #path('user/uprofile/', update_profile, name='customer_update_profile'),
    #path('admin/create-profile',AddProfile.as_view(),name='create_profile'),
    #path('guest-user/',guest_user_view,name='guest_user_register'),
    #path('users/', UsersView.as_view(), name='UserList'),
    #path('create-user/', UserAdminCreationForm, name='CreateUser'),



                ##########Seller################

    #path('users/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup')
    #path('register/seller/',SellerRegister.as_view(),name='SellerRegister'),
]