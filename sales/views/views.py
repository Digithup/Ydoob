import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import generic

from catalog.models.models import Products, Categories, VariantDetails
from sales.models.order import ShopCart, Order, OrderForm, OrderProduct, ShopCartForm
from user.models import User


def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login')  # Check login
def AddToCart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Products.objects.get(pk=id)
    variant = VariantDetails.objects.filter(product=product)

    if variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid,
                                                 user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
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
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Categories.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += int(rs.product.price * rs.quantity)
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               }
    return render(request, 'cart.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")

stripe.api_key = settings.STRIPE_SECRET_KEY

def orderproduct(request):
        category = Categories.objects.all()
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total = 0
        for rs in shopcart:
            if rs.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += int(rs.product.price * rs.quantity)

        if request.method == 'POST':  # if there is a post
            form = OrderForm(request.POST)
            # return HttpResponse(request.POST.items())
            if form.is_valid():
                # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
                # ..............
                #######Payment

                host =request.META['HTTP_HOST']
                checkout_session = stripe.checkout.Session.create(
                    # Customer Email is optional,
                    # It is not safe to accept email directly from the client side
                    # customer_email=request_data['email'],
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount':100,
                                'product_data': {
                                    'name':' rs.product.title',
                                },

                            },
                            'quantity': 1,
                        }
                    ],
                    mode='payment',
                    success_url="http://{}{}".format(host, reverse('sales:PaymentSuccess')),
                    cancel_url="http://{}{}".format(host, reverse('sales:PaymentFailed')),
                )
                #########END####
                data = Order()
                data.first_name = form.cleaned_data['first_name']  # get product quantity from form
                data.last_name = form.cleaned_data['last_name']
                data.address = form.cleaned_data['address']
                data.city = form.cleaned_data['city']
                data.phone = form.cleaned_data['phone']
                data.user_id = current_user.id
                data.total = total
                data.ip = request.META.get('REMOTE_ADDR')
                ordercode = get_random_string(5).upper()  # random cod
                data.code = ordercode
                data.save()  #

                for rs in shopcart:
                    detail = OrderProduct()
                    detail.order_id = data.id  # Order Id
                    detail.product_id = rs.product_id
                    detail.user_id = current_user.id
                    detail.quantity = rs.quantity
                    if rs.variant == 'None':
                        detail.price = rs.product.price
                    else:
                        detail.price = rs.product.price
                    detail.variant_id = rs.variant_id
                    detail.amount = rs.amount
                    detail.save()
                    # ***Reduce quantity of sold product from Amount of Product
                    if rs.variant == 'None':
                        product = Products.objects.get(id=rs.product_id)
                        product.quantity -= rs.quantity
                        product.save()
                    else:
                        product = Products.objects.get(id=rs.product_id)
                        product.quantity = rs.quantity
                        product.save()
                    # ************ <> *****************

                ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
                request.session['cart_items'] = 0
                messages.success(request, "Your Order has been completed. Thank you ")
                return redirect(checkout_session.url, code=303)
                #return render(request, 'payments/payment_success.html', {'ordercode': ordercode, 'category': category})
            else:
                messages.warning(request, form.errors)
                return HttpResponseRedirect("/order/orderproduct")

        form = OrderForm()
        profile = User.objects.get(id=current_user.id)
        context = {'shopcart': shopcart,
                   'category': category,
                   'total': total,
                   'form': form,
                   'profile': profile,
                   }
        return render(request, 'checkout.html', context)





