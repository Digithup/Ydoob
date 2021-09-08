# importing the requests library
import requests
# importing Hash Library
import hashlib
# FawryPayAPI Endpoint
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from sales.models.orders import Order
from sales.models.payment import Payment


class PaymentFawry(LoginRequiredMixin, View):
    '''
    Handle Stripe payment (Stripe API)
    '''

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {

            'order': order
        }
        return render(self.request, 'payments/PaymentFawry.html', context)

    def post(self, *args, **kwargs):
        # Create Stripe payment
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        chargeID = fawry_payment( token, order.total, str(order.code))
        if (chargeID is not None):
            order.ordered = True

            # Save the payment
            payment = Payment()
            payment.stripe_charge_id = chargeID
            payment.user = self.request.user
            payment.price = order.total
            payment.paid= 'True'
            payment.save()
            order.payment = payment
            order.save()
            #return render(request, 'payments/payment_success.html', )
            return redirect('/')
        else:
            messages.error(self.request, "Something went wrong with Stripe. Please try again later")
            return redirect('sales:PaymentFawry',)

def fawry_payment(secret_key, token, amount, description):
    try:
        print(secret_key, token, amount, description, )
        # Use Stripe's library to make requests...
        stripe.api_key = secret_key
        # Token is created using Stripe Checkout or Elements!
        # Get the payment token ID submitted by the form:
        charge = stripe.Charge.create(
            amount=int(amount * 100),
            currency='usd',
            description=description,
            source=token,
        )
        return charge['id']
    except :
        pass
    return None


    URL = "https://atfawry.fawrystaging.com/ECommerceWeb/Fawry/payments/charge"

    # Payment Data
    merchantCode = '1tSa6uxz2nTwlaAmt38enA=='
    merchantRefNum = '99900642041'
    merchant_cust_prof_id = '458626698'
    payment_method = 'CARD'
    amount = '580.55'
    cardNumber = '4005550000000001'
    cardExpiryYear = '21'
    cardExpiryMonth = '05'
    cvv = 123
    merchant_sec_key = '259af31fc2f74453b3a55739b21ae9ef'
    signature = hashlib.sha256(merchantCode + merchantRefNum + merchant_cust_prof_id + payment_method +
                               amount + cardNumber + cardExpiryYear + cardExpiryMonth + cvv + merchant_sec_key).hexdigest()

    # defining a params dict for the parameters to be sent to the API
    PaymentData = {
        'merchantCode': merchantCode,
        'merchantRefNum': merchantRefNum,
        'customerName': 'Ahmed Ali',
        'customerMobile': '01234567891',
        'customerEmail': 'example@gmail.com',
        'customerProfileId': '777777',
        'cardNumber': '4005550000000001',
        'cardExpiryYear': '21',
        'cardExpiryMonth': '05',
        'cvv': '123',
        'amount': '580.55',
        'currencyCode': 'EGP',
        'language': 'en-gb',
        'chargeItems': {
            'itemId': '897fa8e81be26df25db592e81c31c',
            'description': 'Item Description',
            'price': '580.55',
            'quantity': '1'
        },
        'signature': signature,
        'payment_method': 'CARD',
        'description': 'example description'
    }
    # sending post request and saving the response as response object
    status_request = requests.post(url=URL, params=json.dumps(PaymentData))

    # extracting data in json format
    status_response = status_request.json()