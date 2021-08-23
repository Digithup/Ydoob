import stripe as stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import generic

from catalog.models.models import Products, Categories, VariantDetails, Wishlist
from sales.models.order import ShopCart, Order, OrderForm, OrderProduct, ShopCartForm
from user.models import User


def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login')  # Check login
@login_required(login_url='/login') # Check login
def AddToCart(request,id,slug):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Products.objects.get(pk=id)
    variantid = request.POST.get('variantid')
    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shop cart ")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Categories.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum((rs.product.price * rs.quantity ) for rs in shopcart)
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
        if rs.product.variant == 'None':
            product = stripe.Product.create(
                name=rs.product.title,
            description = rs.product.keyword,
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(total*100),
                currency='usd',
            )
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            #######Payment

            host = request.META['HTTP_HOST']

            checkout_session = stripe.checkout.Session.create(
                # Customer Email is optional,
                # It is not safe to accept email directly from the client side
                # customer_email=request_data['email'],
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount':int(total*100),
                            'product_data': {
                                'name': product ,
                            },

                        },
                        'quantity': rs.quantity,
                    }
                ],
                mode='payment',
                success_url="http://{}{}".format(host, reverse('sales:PaymentSuccess')),
                cancel_url="http://{}{}".format(host, reverse('sales:PaymentFailed')),
            )
            #########END####

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #


            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if  rs.product.variant=='None':
                    product = Products.objects.get(id=rs.product_id)
                   # product.quantity -= int(rs.quantity)
                    product.save()
                else:
                    variant = VariantDetails.objects.get(id=rs.variant_id)
                   # variant.quantity -= int(rs.quantity)
                    variant.save()
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return redirect(checkout_session.url, code=303)
            #return render(request, 'payments/payment_success.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form= OrderForm()
    profile = User.objects.get(id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
               }

    return render(request, 'checkout.html', context)





class WishlistView(generic.View):
    def get(self,request, *args, **kwargs):

        wish_item = Wishlist.objects.filter(user=request.user)
        context={
            'wish_item':wish_item
        }
        return render(self.request,'wishlist.html',context)

def addWishlist(request):
    if request.method =="POST":
        product_var_id=request.POST.get('product-id')
        product_var=Products.objects.get(id=product_var_id)
        try:
            wish_item=Wishlist.objects.get(user=request.user , product=product_var)
            if wish_item:
                wish_item.quantity +=1
                wish_item.save()
        except:
            Wishlist.objects.create(user=request.user,product=product_var)
        finally:
            return HttpResponseRedirect(reverse('sales:Wishlist'))

def deletefromWishlist(request, id):
    Wishlist.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Wishlist.")
    return HttpResponseRedirect(reverse('sales:Wishlist'))