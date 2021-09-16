

from django.conf import settings
# for HTML Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.models.setting import Setting
from sales.models.cart import ShopCart
from sales.models.orders import Order, OrderProduct
from vendors.models import Vendor


def notify_admin(data):
    from_email = settings.DEFAULT_EMAIL_FROM
    site_setting=Setting.objects.all()

    for setting in site_setting:
        to_email = setting.email
        subject = 'New Vendor Accepted'
        text_content = 'You have a New Vendor Accepted!'
        html_content = render_to_string('email_notification/email_notify_admin.html', {'data': data, 'vendor': setting})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def notify_user(data):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = data.email
    subject = 'New Vendor Request'
    text_content = 'Thank you for the request!'
    html_content = render_to_string('email_notification/email_notify_user.html', {'data': data})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()