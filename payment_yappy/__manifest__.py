# -*- coding: utf-8 -*-

{
    'name': 'Yappy Payment Acquirer',
    'version': '1.0',
    'category': 'Payment',
    'summary': 'Integration with Yappy Payment Gateway',
    'description': 'Yappy Payment Acquirer for Odoo',
    'author': 'Farmaoffers',
    'website': 'https://www.farmaoffers.com',
    'depends': ['payment', 'website_sale'],
    'data': [

    ],
    'assets': {
        'web.assets_frontend': [
            'payment_yappy/static/src/js/payment_form.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
