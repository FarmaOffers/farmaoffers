{
    'name': 'Farmaoffers Design',
    'version': '1.0.0',
    'author': 'Farmaoffers',
    'category': 'Website',
    'summary': 'Base module for Farmaoffers custom design and snippets',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'web_editor',
        'website_sale',
        'sale_management',
        'sale_stock',
        'stock',
        'product',
    ],
    'data': [
        # === Plantillas base ===
        'views/homepage_templates.xml',

        # === Snippets ===
        'views/snippets/stripe_info_snippet.xml',
        'views/snippets/stripe_info_snippet_registry.xml',
        'views/snippets/top_products_snippet.xml',
        'views/snippets/top_products_snippet_registry.xml',
        'views/h_f_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # === Stripe Info ===
            '/farmaoffers_design/static/src/snippets/stripe_info/style.scss',
            '/farmaoffers_design/static/src/snippets/stripe_info/000.js',

            # === Top Products ===
            '/farmaoffers_design/static/src/snippets/top_products/top_products.scss',
            '/farmaoffers_design/static/src/snippets/top_products/000.js',
        ],
        'web_editor.assets_wysiwyg': [
            # JS habilitado en modo editor
            '/farmaoffers_design/static/src/snippets/stripe_info/000.js',
            '/farmaoffers_design/static/src/snippets/top_products/000.js',
        ],
    },
    'installable': True,
    'application': False,
}