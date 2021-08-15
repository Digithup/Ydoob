import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotFound, JsonResponse, request, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from stripe import Product

from sales.models.order import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret=settings.STRIPE_WEBHOOK_SECRET

class create_checkout_session(generic.View):
    def post(self, request, *args, **kwargs):
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
                            'name': 'product title',
                        },

                    },
                    'quantity': 2,
                }
            ],
            mode='payment',
            success_url="http://{}{}".format(host, reverse('sales:PaymentSuccess')),
            cancel_url="http://{}{}".format(host, reverse('sales:PaymentFailed')),
        )

        # return JsonResponse({'data': checkout_session})
        return redirect(checkout_session.url, code=303)


class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        messages.success(request, "Your Order has been completed. Thank you ")
        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


def PaymentSuccess(request):
    context = {
        'payment_status': 'success'
    }

    return render(request, 'payments/payment_success.html', context)


class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")


class OrderHistoryListView(ListView):
    model = Order
    template_name = "payments/order_history.html"
