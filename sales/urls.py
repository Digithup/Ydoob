from django.urls import path

from sales.views import views
from sales.views.cart import updateItem
from sales.views.payment import PaymentSuccessView, PaymentFailedView, OrderHistoryListView, create_checkout_session, \
    PaymentSuccess, my_webhook_view
from sales.views.views import shopcart

app_name = 'sales'

urlpatterns = [
    path('cart/', views.index, name='index'),
    path('cart/addtoshopcart/<int:id>', views.AddToCart, name='AddToCart'),
    path('cart/deletefromcart/<int:id>', views.deletefromcart, name='DeleteFromCart'),
    path('cart/update_item/', updateItem, name="update_item"),

    path('cart/orderproduct/', views.orderproduct, name='OrderProduct'),
    path('shopcart/', shopcart, name='ShopCart'),


    ##############Payment#####################
    path('cart/success/', PaymentSuccess, name='PaymentSuccess'),
    path('failed/', PaymentFailedView.as_view(), name='PaymentFailed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),

    path('api/checkout-session/', create_checkout_session.as_view(), name='OrderStripe'),
    path('api/webhookstripe/', my_webhook_view, name='WebhookStripe'),
]