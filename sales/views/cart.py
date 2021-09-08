import json
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models

# Create your models here.
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from catalog.models.models import Products, Categories
from sales.forms.forms import ShopCartForm
from sales.models.cart import Wishlist, ShopCart



class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action:', action)
#     print('Product:', productId)
#
#     customer = request.user.customer
#     product = Products.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
#
#     orderItem.save()
#
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#
#     return JsonResponse('Item was added', safe=False)


class WishlistView(generic.View):
    def get(self, request, *args, **kwargs):
        wish_item = Wishlist.objects.filter(user=request.user)
        context = {
            'wish_item': wish_item
        }
        return render(self.request, 'wishlist.html', context)


def addWishlist(request):
    if request.method == "POST":
        product_var_id = request.POST.get('product-id')
        product_var = Products.objects.get(id=product_var_id)
        try:
            wish_item = Wishlist.objects.get(user=request.user, product=product_var)
            if wish_item:
                wish_item.quantity += 1
                wish_item.save()
        except:
            Wishlist.objects.create(user=request.user, product=product_var)
        finally:
            return HttpResponseRedirect(reverse('sales:Wishlist'))


def deletefromWishlist(request, id):
    Wishlist.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Wishlist.")
    return HttpResponseRedirect(reverse('sales:Wishlist'))


@login_required(login_url='/login')  # Check login
def AddToCart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Products.objects.get(pk=id)
    variantid = request.POST.get('variant')  # from variant add to cart
    vendorid = request.POST.get('vendor')

    if product.variant != 'None':

        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id,vendor_id=vendorid)  # Check product in shopcart

        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id,vendor_id=vendorid)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id,vendor_id=vendorid)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id,vendor_id=vendorid)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.store_id = vendorid
                data.quantity = form.cleaned_data['quantity']

                data.save()
            messages.success(request, "Product added to Shopcart 4",request.POST)
            print(request.POST)
            return HttpResponseRedirect(url)
        else:

            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
            return HttpResponseRedirect(url)
    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.store_id = vendorid
            data.save()  #
        messages.success(request, "Product added to Shopcart3")
        return HttpResponseRedirect(url)


def index(request):
    return HttpResponse("Orders Page")


def shopcart(request):
    category = Categories.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             }
    return render(request,'cart.html',context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")