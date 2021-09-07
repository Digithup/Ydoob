from django.test import TestCase

# Create your tests here.
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
                            'unit_amount': 100,
                            'product_data': {
                                'name': ' rs.product.title',
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
                detail.order_id = data.id  # Orders Id
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
            messages.success(request, "Your Orders has been completed. Thank you ")
            return redirect(checkout_session.url, code=303)
            # return render(request, 'payments/payment_success.html', {'ordercode': ordercode, 'category': category})
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