from django.urls import path

from sales.views import views
from sales.views.cart import updateItem
from sales.views.payment import PaymentFailedView, OrderHistoryListView, create_checkout_session, \
    PaymentSuccess, my_webhook_view, StripeIntentView, CreateCheckoutSessionView, stripe_webhook, CancelView, \
    SuccessView
from sales.views.views import shopcart, WishlistView, addWishlist, deletefromWishlist

app_name = 'sales'

urlpatterns = [
    path('cart/', views.index, name='index'),
    path('cart/addtoshopcart/<int:id>/<slug:slug>', views.AddToCart, name='AddToCart'),
    path('cart/deletefromcart/<int:id>', views.deletefromcart, name='DeleteFromCart'),
    path('cart/orderproduct/', views.orderproduct, name='OrderProduct'),
    path('shopcart/', shopcart, name='ShopCart'),
    path('cart/update_item/', updateItem, name="update_item"),

##############wishlist#####################
    path('cart/wishlist/', WishlistView.as_view(), name="Wishlist"),
    path('cart/addwishlist/', addWishlist, name="AddWishlist"),
    path('cart/deletefromwishlist/<int:id>', deletefromWishlist, name='DeleteFromWishlist'),



    ##############Payment#####################
    path('cart/success/', PaymentSuccess, name='PaymentSuccess'),
    path('failed/', PaymentFailedView.as_view(), name='PaymentFailed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),

    path('api/checkout-session/', create_checkout_session.as_view(), name='OrderStripe'),
    path('api/webhookstripe/', my_webhook_view, name='WebhookStripe'),

    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),

    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
