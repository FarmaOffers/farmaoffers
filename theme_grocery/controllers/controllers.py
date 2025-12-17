# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression
from odoo.http import request, route
from odoo import SUPERUSER_ID


class website_sale(WebsiteSale):

    def _check_float(self, val):
        try:
            return float(val)
        except ValueError:
            pass
        return False

    def _get_search_domain(self, search, category, attrib_values):
        domains = super(website_sale, self)._get_search_domain(search, category, attrib_values)

        # Price
        min_price = request.httprequest.args.get('min_price')
        max_price = request.httprequest.args.get('max_price')
        if min_price:
            min_price = self._check_float(min_price)
            if min_price:
                domains = expression.AND([domains, [('list_price', '>=', min_price)]])
        if max_price:
            max_price = self._check_float(max_price)
            if max_price:
                domains = expression.AND([domains, [('list_price', '<=', max_price)]])
        if request.httprequest.args.get('under_10'):
            domains = expression.AND([domains, [('list_price', '<=', 10)]])
        if request.httprequest.args.get('ten_to_tweenty'):
            domains = expression.AND([domains, ['&', ('list_price', '>=', 10), ('list_price', '<=', 20)]])
        if request.httprequest.args.get('over_20'):
            domains = expression.AND([domains, [('list_price', '>=', 20)]])

        return domains

    @route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super(website_sale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )
        att_items = res.qcontext.get('attrib_values') or []
        att_items = list(set(tuple(item) for item in att_items))
        website = request.website
        langs = website.language_ids or request.env['res.lang'].sudo().search([('website_published', '=', True)])

        # Build list same shape as your template expects: (code, code, name)
        language_ids = [(lang.code, lang.code, lang.name) for lang in langs]

        new_list = {}
        for item in att_items:
            if item[0] in new_list:
                new_list[item[0]].append(item[1])
            else:
                new_list[item[0]] = [item[1]]

        attr_filters = {}
        for attr in new_list:
            attr_name = request.env['product.attribute'].browse(attr).name
            attr_values = []
            for att_value_id in new_list[attr]:
                attr_value = request.env['product.attribute.value'].browse(att_value_id).name
                attr_values.append((attr_value, f"{attr}-{att_value_id}"))
            attr_filters[attr_name] = attr_values

        res.qcontext['attr_filters'] = attr_filters
        res.qcontext['language_ids'] = language_ids
        return res

    @route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_json(
        self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
        product_custom_attribute_values=None, no_variant_attribute_value_ids=None, **kwargs
    ):
        res = super(website_sale, self).cart_update_json(
            product_id=product_id, line_id=None, add_qty=add_qty, set_qty=set_qty, display=display)
        order = request.website.sale_get_order()
        if order.order_line:
            amount = "{:0.2f}".format(order.amount_total)
            res['cart_amount'] = order.currency_id.symbol + ' ' + amount
        return res

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'],
                website=True, multilang=False)
    def cart_options_update_json(self, product_and_options, goto_shop=None, lang=None, **kwargs):
        res = super(website_sale, self).cart_options_update_json(
            product_and_options, goto_shop, lang, **kwargs)
        res = {}
        order = request.website.sale_get_order()
        if order.order_line:
            amt = "{:0.2f}".format(order.amount_total)
            amount = order.currency_id.symbol + ' ' + amt
            res = '{"cart_quantity": "%s", "cart_amount": "%s"}' % (
                str(order.cart_quantity), amount)
        return res

    @http.route(['/add/quick/views/popup'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def quick_views_popup(self, product_id, **kw):
        values = {}
        if product_id:
            product = request.env['product.template'].browse(product_id)
            combination = product._get_first_possible_combination()
            combination_info = product._get_combination_info(
                combination=combination,
                add_qty=1,
            )
            values['data'] = request.env['ir.ui.view']._render_template(
                "theme_grocery.p_detail_quick_view_model",
                {
                    'product': product,
                    'combination': combination,
                    'combination_info': combination_info,
                }
            )
        return values


class WebsiteTestimonial(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def homepage(self, **kw):
        website = request.website
        env = request.env

        # Check if the grocery theme module is installed
        theme_module = env['ir.module.module'].search([('name', '=', 'theme_grocery')], limit=1)
        template_exists = env['ir.ui.view'].search([('key', '=', 'website.grocery_homepage')], limit=1)
        if theme_module and theme_module.state == 'installed' and template_exists:
            testimonials = env['customer.testimonial'].search([], order='sequence')
            sliders = env['homepage.slider'].search([], order='sequence')
            langs = website.language_ids or env['res.lang'].search([('website_published', '=', True)])
            language_ids = [(lang.code, lang.code, lang.name) for lang in langs]

            return request.render('website.grocery_homepage', {
                'testimonials': testimonials,
                'sliders': sliders,
                'language_ids': language_ids,
                'frontend_languages': langs,
            })

        return request.render('website.homepage')
