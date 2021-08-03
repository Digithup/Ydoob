from django.conf.urls import url
from django.urls import path

from sales.views import views ,order , cart
from sales.views.cart import updateItem
from sales.views.views import shopcart

app_name = 'sales'

urlpatterns = [
    path('cart/', views.index, name='index'),
    path('cart/addtoshopcart/<int:id>', views.AddToCart, name='AddToCart'),
    path('cart/deletefromcart/<int:id>', views.deletefromcart, name='DeleteFromCart'),
    path('cart/update_item/', updateItem, name="update_item"),

    path('cart/orderproduct/', views.orderproduct, name='OrderProduct'),
    path('shopcart/', shopcart, name='ShopCart'),
]