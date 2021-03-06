from django.urls import path

import sales.views.cart
from sales.views import views
from sales.views.PaymentGateway.paymob_payment import PaymentMyPaymob
from sales.views.cart import  WishlistView, addWishlist, deletefromWishlist, shopcart
from sales.views.PaymentGateway.fawry_payment import PaymentFawry
from sales.views.payment import PaymentFailedView, OrderHistoryListView, create_checkout_session, \
    PaymentSuccess, my_webhook_view, StripeIntentView, CreateCheckoutSessionView, stripe_webhook, CancelView, \
    SuccessView
from sales.views.views import PaymentView
from sales.views.PaymentGateway.stripe_payment import PaymentStripe

app_name = 'sales'

urlpatterns = [
    path('cart/', sales.views.cart.index, name='index'),
    path('cart/addtoshopcart/<int:id>', sales.views.cart.AddToCart, name='AddToCart'),
    path('cart/deletefromcart/<int:id>', sales.views.cart.deletefromcart, name='DeleteFromCart'),
    #path('cart/orderproduct/', views.orderproduct, name='Checkout'),
    path('cart/orderproduct/', views.Checkout, name='Checkout'),
    path('shopcart/', shopcart, name='ShopCart'),
    #path('cart/update_item/', updateItem, name="update_item"),

##############wishlist#####################
    path('cart/wishlist/', WishlistView, name="Wishlist"),
    path('cart/addwishlist/', addWishlist, name="AddWishlist"),
    path('cart/deletefromwishlist/<int:id>', deletefromWishlist, name='DeleteFromWishlist'),



    ##############Payment#####################
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),


    path('payment/', PaymentStripe.as_view(), name='PaymentStripe'),
    path('PaymentFawry/', PaymentMyPaymob.as_view(), name='PaymentMyPaymob'),
    path('PaymentFawry/', PaymentFawry.as_view(), name='PaymentFawry'),



    path('api/checkout-session/', create_checkout_session.as_view(), name='OrderStripe'),
    path('api/webhookstripe/', my_webhook_view, name='WebhookStripe'),
    path('cart/success/', PaymentSuccess, name='PaymentSuccess'),
    path('failed/', PaymentFailedView.as_view(), name='PaymentFailed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),






]
