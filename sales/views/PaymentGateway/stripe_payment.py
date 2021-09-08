import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from sales.models.orders import Order
from sales.models.payment import Payment


class PaymentStripe(LoginRequiredMixin, View):
    '''
    Handle Stripe payment (Stripe API)
    '''

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'order': order
        }
        return render(self.request, 'payments/PaymentStripe.html', context)

    def post(self, *args, **kwargs):
        # Create Stripe payment
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        chargeID = stripe_payment(settings.STRIPE_SECRET_KEY, token, order.total, str(order.code))
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
            return redirect('sales:PaymentStripe',)


def stripe_payment (secret_key, token, amount, description ):
    try:
        print(secret_key, token, amount, description, )
        # Use Stripe's library to make requests...
        stripe.api_key = secret_key
        # Token is created using Stripe Checkout or Elements!
        # Get the payment token ID submitted by the form:
        charge = stripe.Charge.create(
            amount= int (amount * 100),
            currency='usd',
            description=description,
            source=token,
        )
        return charge['id']
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print('Status is: %s' % e.http_status)
        print('Code is: %s' % e.code)
        # param is '' in this case
        print('Param is: %s' % e.param)
        print('Message is: %s' % e.user_message)
    except stripe.error.RateLimitError as e:
        print (e)
    except stripe.error.InvalidRequestError as e:
        print (e)

    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print (e)

    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print (e)

    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print (e)

    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print (e)

    return None


