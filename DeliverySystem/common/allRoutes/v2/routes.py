from django.urls import reverse_lazy
from django.conf import settings


all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('vendor-home'),
        'superuser': False,
        'icon': 'fa fa-dashboard',
        'service': '',
        'groups': False,
        'permission': ''
    },
    {
        'title': 'groups and permissions',
        'url': reverse_lazy('vendor-groups'),
        'superuser': False,
        'icon': 'fa fa-users',
        'service': '',
        'groups': False,
        'permission': 'auth.view_group'
    },
    {
        'title': 'users',
        'url': reverse_lazy('vendor-users'),
        'service': '',
        'superuser': False,
        'icon': 'fa fa-user',
        'groups': False,
        'permission': 'api.view_user'
    },
    {
        'groups': True,
        'title': 'products',
        'superuser': False,
        'icon': 'fa fa-sitemap',
        'service': '',
        'permission': '',
        'links': [
            {
                'title': 'category',
                'url': reverse_lazy('category'),
                'permission': 'Products.view_category'
            },
            {
                'title': 'products',
                'url': reverse_lazy('products'),
                'permission': 'Products.view_product'
            },
        ]
    },
    {
        'groups': True,
        'title': 'orders',
        'superuser': False,
        'icon': 'fa fa-cart-plus',
        'service': '',
        'permission': '',
        'links': [
            {
                'title': 'pending/new orders',
                'url': reverse_lazy('vendor-orders'),
                'permission': 'OrderAndDelivery.view_orders'
            },
            {
                'title': 'delivered orders',
                'url': reverse_lazy('vendor-delivered'),
                'permission': 'OrderAndDelivery.view_orders'
            },
        ]
    }
]

if settings.MULTI_VENDOR:
    all_navigation_routes += [
        {
            'groups': True,
            'title': 'vendor management',
            'superuser': True,
            'icon': 'fa fa-object-groups',
            'permission': 'Vendor.view_vendor',
            'service': 'multi-vendor',
            'links': [
                {
                    'title': 'vendors',
                    'url': reverse_lazy('vendor-vendors'),
                    'permission': 'Vendor.view_vendor'
                },
                {
                    'title': 'delivered orders',
                    'url': reverse_lazy('vendor-delivered'),
                    'permission': 'OrderAndDelivery.view_orders'
                },
            ]
        }
    ]


if settings.HAS_OFFER_APP:
    all_navigation_routes += [
        {
            'title': 'special offers',
            'superuser': False,
            'icon': 'fa fa-users',
            'service': '',
            'groups': True,
            'permission': '',
            'links': [
                {
                    'title': 'all offers',
                    'url': reverse_lazy('vendor-offers'),
                    'permission': 'Offer.view_offer'
                },
                {
                    'title': 'participate in offers',
                    'url': reverse_lazy('vendor-offers'),
                    'permission': 'Offer.view_offer'
                },
            ]
        }
    ]

all_navigation_routes += [
    {
        'title': 'company information',
        'url': reverse_lazy('vendor-company-info'),
        'superuser': False,
        'icon': 'fa fa-info',
        'service': '',
        'groups': False,
        'permission': 'CompanyInformation.view_companyinformation'
    },
]