# -*- coding: utf-8 -*-

{
    'name': 'Yappy Payment Acquirer',
    'version': '1.0',
    'category': 'Payment',
    'summary': 'Integration with Yappy Payment Gateway',
    'description': 'Yappy Payment Acquirer for Odoo',
    'author': 'Rootstack, S.A.',
    'depends': ['payment'],
    'data': [
        'views/payment_yappy_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
        ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'external_dependencies': {
        'python': ['pynpm'],
    }
}
