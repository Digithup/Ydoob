from django.urls import path

from DeliverySystem.courier import views as courier_views, apis as courier_apis
from DeliverySystem.customer import views as customer_views
from DeliverySystem.views.dashboard import DeliveryDashboard, DeliveryOrder, DeliveryLoginView, DeliverySignup, \
    DeliveryLogout

app_name = 'DeliverySystem'

urlpatterns = [
    path('login/', DeliveryLoginView.as_view(), name="DeliveryLogin"),
    path('login/', DeliverySignup, name='DeliveryRegister'),
    path('logout/', DeliveryLogout, name='DeliveryLogout'),

    path('', DeliveryDashboard, name="DeliveryIndex"),
    path('orders', DeliveryOrder, name="DeliveryOrder"),

    ##############courier_views###############
    path('orders/available/', courier_views.available_jobs_page, name="AvailableOrders"),
    path('orders/available/<id>/', courier_views.available_job_page, name="AvailableOrder"),

    path('create_order/<str:code>/', customer_views.create_order_page, name="CreateOrder"),
    path('orders/current/', courier_views.current_job_page, name="CurrentOrder"),
    path('orders/archived/', courier_views.archived_jobs_page, name="ArchivedOrder"),

    path('api/jobs/available/', courier_apis.available_jobs_api, name="available_jobs_api"),
    path('orders/complete/', courier_views.job_complete_page, name="OrderComplete"),

    path('orders/current/<id>/take_photo/', courier_views.current_job_take_photo_page, name="current_job_take_photo"),

    path('profile/', courier_views.profile_page, name="profile"),
    path('payout_method/', courier_views.payout_method_page, name="payout_method"),

    path('api/jobs/current/<id>/update/', courier_apis.current_job_update_api, name="current_job_update_api"),
    path('api/fcm-token/update/', courier_apis.fcm_token_update_api, name="fcm_token_update_api"),

    ##############courier_views###############
    # path('', customer_views.home, name="customer_home"),
    path('profile/', customer_views.profile_page, name="profile"),
    # path('create_job/', customer_views.create_job_page, name="create_job"),
    path('payment_method/', customer_views.payment_method_page, name="payment_method"),

    path('jobs/current/', customer_views.current_jobs_page, name="current_jobs"),
    path('jobs/archived/', customer_views.archived_jobs_page, name="archived_jobs"),
    path('jobs/<job_id>/', customer_views.job_page, name="job"),

    path('courier', courier_views.home, name="CourierIndex"),

]
