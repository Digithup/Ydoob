from sales.models.cart import ShopCart
from sales.views.cart import Cart, shopcart


def cart(request):
    current_user = request.user  # Access User Session information
    return {'cart': Cart(request),'shopcart':ShopCart.objects.filter(user_id=current_user.id)}