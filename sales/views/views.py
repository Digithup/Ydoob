import stripe as stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from catalog.models.models import Products, Variants
from notification.utilities import create_notification
from sales.forms.forms import CheckoutForm
from sales.models.cart import ShopCart

from sales.models.orders import OrderProduct, PaymentMethods, Order
from user.models import UserAddress
from vendors.models import Vendor

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


# @login_required
# def orderproduct(request):
#     category = Categories.objects.all()
#     current_user = request.user
#     shopcart = ShopCart.objects.filter(user_id=current_user.id)
#     total = 0
#
#     for rs in shopcart:
#         if rs.product.variant == 'None':
#             product = stripe.Product.create(
#                 name=rs.product.title,
#                 description=rs.product.keyword,
#             )
#             price = stripe.Price.create(
#                 product=product.id,
#                 unit_amount=int(total * 100),
#                 currency='usd',
#             )
#             total += rs.product.price * rs.quantity
#         else:
#             total += rs.variant.price * rs.quantity
#
#     if request.method == 'POST':  # if there is a post
#         form = CheckoutForm(request.POST)
#         # return HttpResponse(request.POST.items())
#         if form.is_valid():
#             # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
#             # ..............
#             #######Payment
#
#             # #host = request.META['HTTP_HOST']
#             #
#             # checkout_session = stripe.checkout.Session.create(
#             #     # Customer Email is optional,
#             #     # It is not safe to accept email directly from the client side
#             #     # customer_email=request_data['email'],
#             #     payment_method_types=['card'],
#             #     line_items=[
#             #         {
#             #             'price_data': {
#             #                 'currency': 'usd',
#             #                 'unit_amount': int(total * 100),
#             #                 'product_data': {
#             #                     'name': product,
#             #                 },
#             #
#             #             },
#             #             'quantity': rs.quantity,
#             #         }
#             #     ],
#             #     mode='payment',
#             #     success_url="http://{}{}".format(host, reverse('sales:PaymentSuccess')),
#             #     cancel_url="http://{}{}".format(host, reverse('sales:PaymentFailed')),
#             # )
#             #########END####
#
#             data = Order()
#             # data.first_name = form.cleaned_data['first_name'] #get product quantity from form
#             # data.last_name = form.cleaned_data['last_name']
#             # data.address = form.cleaned_data['address']
#             address=request.POST.get('address')
#             address= UserAddress.objects.get(address_title=address)
#             data.address = address
#
#             data.user_id = current_user.id
#             data.total = total
#             data.ip = request.META.get('REMOTE_ADDR')
#             ordercode = get_random_string(5).upper()  # random cod
#             data.code = ordercode
#             data.save()  #
#
#             for rs in shopcart:
#                 detail = OrderProduct()
#                 detail.order_id = data.id  # Orders Id
#                 detail.product_id = rs.product_id
#                 detail.user_id = current_user.id
#                 detail.quantity = rs.quantity
#                 if rs.product.variant == 'None':
#                     detail.price = rs.product.price
#                 else:
#                     detail.price = rs.variant.price
#                 detail.variant_id = rs.variant_id
#                 detail.amount = rs.amount
#                 detail.save()
#                 # ***Reduce quantity of sold product from Amount of Product
#                 if rs.product.variant == 'None':
#                     product = Products.objects.get(id=rs.product_id)
#                     # product.quantity -= int(rs.quantity)
#                     product.save()
#                 else:
#                     variant = Variants.objects.get(id=rs.variant_id)
#                     # variant.quantity -= int(rs.quantity)
#                     variant.save()
#                 # ************ <> *****************
#
#             #ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
#             #request.session['cart_items'] = 0
#             messages.success(request, "Your Orders has been completed. Thank you ")
#             #return redirect(checkout_session.url, code=303)
#             return render(request, 'payments/payment_success.html',{'ordercode':ordercode,'category': category})
#         else:
#             messages.warning(request, form.errors)
#             return HttpResponseRedirect(reverse('sales:OrderProduct'))
#
#     form = CheckoutForm()
#     profile = User.objects.get(id=current_user.id)
#     address = UserAddress.objects.filter(user=current_user)
#     context = {'shopcart': shopcart,
#                'category': category,
#                'total': total,
#                'form': form,
#                'profile': profile,
#                'address': address,
#                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
#                }
#
#     return render(request, 'checkout.html', context)


@login_required
def Checkout(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0

    for rs in shopcart:
        if rs.product.variant == 'None':

            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = CheckoutForm(request.POST)

        if form.is_valid():

            print(request.POST)
            address = request.POST.get('address')
            address = UserAddress.objects.get(id=address)
            payment_method = request.POST.get('payment_method')
            payment_method = PaymentMethods.objects.get(id=payment_method)
            data = Order()
            data.address = address
            data.payment_method = payment_method
            print(request.POST)

            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()  #

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Orders Id
                detail.product_id = rs.product_id
                vendor = Vendor.objects.get(vendor=rs.product.seller)
                detail.vendor = vendor
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id = rs.variant_id
                detail.amount = rs.amount
                print(request.POST)
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if rs.product.variant == 'None':
                    product = Products.objects.get(id=rs.product_id)
                    # product.quantity -= int(rs.quantity)
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.variant_id)
                    # variant.quantity -= int(rs.quantity)
                    variant.save()
                # ************ <> *****************
                create_notification(request, detail.vendor.vendor, 'NewOrder', extra_id=detail.id,extra_info=rs.product)

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Orders has been completed. Thank you ")

            # return render(request, 'payments/payment_success.html',{'ordercode':ordercode,'category': category})
            return redirect('sales:payment', payment_option=payment_method)
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(reverse('sales:Checkout'))

    form = CheckoutForm()
    profile = User.objects.get(id=current_user.id)
    address = UserAddress.objects.filter(user=current_user)
    context = {'shopcart': shopcart,
               'total': total,
               'form': form,
               'profile': profile,
               'address': address,

               }

    return render(request, 'checkout.html', context)


class PaymentView(LoginRequiredMixin, View):
    '''
    Handle Stripe payment (Stripe API)
    '''

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, status='New').last()
        payment_method = PaymentMethods.objects.get(id=order.payment_method.id)
        print(payment_method)
        if payment_method.method == "COD":
            print('cod')
            return render(request, 'payments/payment_success.html', )
        elif payment_method.method == 'Stripe':
            print('Stripe')
            return redirect('sales:PaymentStripe', )
        elif payment_method.method == 'Fawry':
            print('Fawry')
            return redirect('sales:PaymentFawry', )

        elif payment_method.method == 'Paymob':
            print(payment_method)
            return redirect('sales:PaymentMyPaymob', )
        elif payment_method.method is None:
            print('none')
            return HttpResponse('error')
        else:
            return HttpResponse('error thing')




