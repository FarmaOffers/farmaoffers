# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

{
    'name': 'Theme Grocery',
    'version': '18.0.1.0',
    'summary': 'One of the finest website ecommerce theme which suits many nature of businesses out of box | Theme | Appearance | Ecommerce | Sales | Online Website | Website Theme | Grocery Theme | Vegetable Shop theme | Food Stall Theme | Buy Online Store Theme| ',
    'description': """
Theme Grocery
==============
Online Supermarket includes on-line vegetable store, foods and groceries available on-line on-line.
    """,
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://kanakinfosystems.com',
    'category': 'Theme/Grocery',
    'depends': [
        'website_sale_wishlist', 'website_sale_comparison',
        'website_blog', 'website_mass_mailing'],
    'demo': [
        'demo/theme_grocery_demo.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/customize_show_templates.xml',
        'views/h_f_templates.xml',
        'views/homepage_templates.xml',
        'views/shop_templates.xml',
        'views/product_details_templates.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_grocery/static/src/scss/style.scss',
            'theme_grocery/static/src/scss/button/style1.scss',
            'theme_grocery/static/src/scss/button/style2.scss',
            'theme_grocery/static/description/favicon.ico',
            'theme_grocery/static/lib/ion.rangeSlider-2.3.1/css/ion.rangeSlider.css',
            'theme_grocery/static/lib/OwlCarousel/owl.carousel.min.css',
            'theme_grocery/static/lib/malihu-custom-scrollbar/jquery.mCustomScrollbar.min.css',
            'theme_grocery/static/src/css/style.css',
            'theme_grocery/static/src/js/website_sale.js',
            'theme_grocery/static/src/js/quick_view_dialog.js',
            'theme_grocery/static/src/js/price_filter.js',
            'theme_grocery/static/lib/ion.rangeSlider-2.3.1/js/ion.rangeSlider.js',
            'theme_grocery/static/lib/OwlCarousel/owl.carousel.min.js',
            'theme_grocery/static/lib/malihu-custom-scrollbar/jquery.mCustomScrollbar.concat.min.js',
            'theme_grocery/static/src/js/script.js',
        ],
    },
    'images': [
        'static/description/theme_grocery.jpg',
        'static/description/theme_grocery_screenshot.jpg'
    ],
    'installable': True,
    'application': True,
    'price': 100,
    'currency': 'EUR'
}
