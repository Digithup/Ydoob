from django.db.models import Sum

from catalog.models.models import Products
from core.models.setting import Setting
from sales.models.orders import Order
from vendors.models import Vendor


def core_processors(request):
    try:
        return {
                'setting': Setting.objects.filter(status=True),
        }
    except Exception as e:
        return {
            'setting': None,
                }
#total_filter = Order.objects.filter(ordered=True).aggregate(total_price=Sum('total')),
#  total_fix = Order.objects.aggregate(TOTAL=Sum('total'))['TOTAL']


def admin_summary(request):
    try:
        total_fix = Order.objects.filter(status='Completed',ordered=True).aggregate(TOTAL=Sum('total'))['TOTAL']

        return {
                #'admin_earnings_total': Order.objects.filter(status='New').aggregate(total=sum('total')),
            #'admin_earnings_total': Order.objects.aggregate(total_price=Sum('total')),
            'admin_earnings_total': total_fix,
            'admin_products_count': Products.objects.all().count(),
            'need_active': Setting.objects.filter(status=True),
            'new_vendor': Vendor.objects.filter(status=True,activation=True).count(),
            'pending_vendor': Vendor.objects.filter(status=False, activation=True).count(),
            'admin_order_total': Order.objects.all()[:5],
        }
    except Exception as e:
        return {
            #'admin_earnings_total':  Order.objects.aggregate(total=Sum('total')),
            'admin_products_count': Products.objects.all().count(),
            'need_active': Setting.objects.filter(status=True),
            'new_vendor': Setting.objects.filter(status=True),
                }

def admin_chart(request):
    try:
        order = Order.objects.values('address', 'total', 'payment_method')
        print(order)
        data = {
            'data': [
                {
                    'address': item['address'],
                    'total': float(item['total']),
                    'payment_method': item['payment_method'],
                }
                for item in order
            ]
        }

        return {

            'admin_orders_location': data,

        }
    except Exception as e:
        return {

            'admin_orders_location': None,

                }
