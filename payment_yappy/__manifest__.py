# -*- coding: utf-8 -*-

{
    'name': 'Yappy Payment Acquirer',
    'version': '1.0',
    'category': 'Payment',
    'summary': 'Integration with Yappy Payment Gateway',
    'description': 'Yappy Payment Acquirer for Odoo',
    'author': 'Farmaoffers',
    'website': 'https://www.farmaoffers.com',
    'depends': ['payment'],
    'data': [
        'data/payment_acquirer_data.xml',
    ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'post_init_hook': '_post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'external_dependencies': {
        'python': ['pynpm'],
    }
}
