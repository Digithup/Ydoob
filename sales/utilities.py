

from django.conf import settings
# for HTML Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from sales.models.cart import ShopCart
from sales.models.orders import Order, OrderProduct
from vendors.models import Vendor


def notify_vendor(detail):
    from_email = settings.DEFAULT_EMAIL_FROM
    vendors=Vendor.objects.filter(orderproduct=detail)

    for vendor in vendors:
        to_email = vendor.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('notify/email_notify_vendor.html', {'data': detail, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def notify_customer(data):
    from_email = settings.DEFAULT_EMAIL_FROM
    data = Order.objects.get(id=data.id)
    to_email = data.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('notify/email_notify_customer.html', {'data': data})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()