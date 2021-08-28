from django.conf.urls import url
from django.urls import path


from .views.user import UserSignup, UserActivate, UserLogin, UserLogout, UserProfile, UpdateImage, UpdateProfile, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, address_list, \
    DeleteAddress, UpdateAddress, CreateAddress

app_name = 'user'

urlpatterns = [

    #path('guest-user/', guest_user_view, name='guest_user_register'),

    ##########User################
    path('signup/', UserSignup, name='CustomerRegister'),
    path('activate/<uidb64>/<token>/', UserActivate, name='activate'),
    path('login/', UserLogin.as_view(), name='CustomerLogin'),
    path('logout/', UserLogout, name='CustomerLogout'),


    ##################Profile#################
    path('user/profile/<slug:slug>', UserProfile, name='UserProfile'),
    path('user/uproile/<slug:slug>', UpdateImage, name='UpdateImage'),
    path('user/uprofile/<slug:slug>', UpdateProfile, name='UpdateProfile'),



    ###########Password###########
    path('reset_password/', PasswordResetView.as_view(), name="ResetPassword"),
    path('reset_password_sent/',  PasswordResetDoneView.as_view(), name="passwordResetDone"),
    path('reset/<uidb64>/<token>/',  PasswordResetConfirmView.as_view(),  name="passwordResetConfirm"),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(),  name="passwordResetComplete"),


    ##########Address################
    path('user/booklist/', address_list, name='address_list'),
    path('user/cadress/', CreateAddress, name='CreateAddress'),
    path('user/adress/<int:pk>', DeleteAddress, name='DeleteAddress'),
    url(r'^user/adress/(?P<pk>\d+)/update/$', UpdateAddress, name='UpdateAddress'),



]
