import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class FarmaoffersThemeCheckout(http.Controller):

    @http.route('/fo/branches', type='http', auth='public', website=True, csrf=False)
    def fo_branches(self, **kw):
        branches = request.env['multi.branch'].sudo().search([], order='name')
        payload = [{'id': b.id, 'name': b.name} for b in branches]
        return request.make_response(
            json.dumps(payload),
            headers=[('Content-Type', 'application/json; charset=utf-8')]
        )

class FarmaoffersWebsiteSale(WebsiteSale):
    """Override para prevenir auto-agregar delivery line en modo pickup"""
    
    @http.route()
    def checkout(self, **post):
        """Override del checkout para remover delivery line si es modo branch"""
        order = request.website.sale_get_order()
        
        # Si estamos en modo branch, asegurar que NO haya delivery line
        if order and order.shipping_mode == 'branch':
            order.sudo().write({'carrier_id': False})
            order.sudo()._remove_delivery_line()
        
        # Llamar al método original
        return super(FarmaoffersWebsiteSale, self).checkout(**post)


class FarmaoffersCheckoutShipping(http.Controller):

    @http.route('/fo/checkout/set_shipping', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def fo_set_shipping(self, **kw):
        order = request.website.sale_get_order()
        if not order:
            return request.make_response(
                json.dumps({'ok': False, 'error': 'no_order'}),
                headers=[('Content-Type','application/json; charset=utf-8')]
            )

        try:
            data = json.loads(request.httprequest.data.decode('utf-8') or '{}')
        except Exception:
            data = {}

        pickup = bool(data.get('pickup'))
        branch_id = data.get('branch_id')

        if pickup:
            # MODO PICKUP: remover delivery
            order.sudo().write({
                'shipping_mode': 'branch',
                'branch_id': int(branch_id) if branch_id else False,
                'carrier_id': False,
            })
            order.sudo()._remove_delivery_line()

            return request.make_response(
                json.dumps({'ok': True, 'mode': 'branch'}),
                headers=[('Content-Type','application/json; charset=utf-8')]
            )

        # MODO ADDRESS: solo guardar el modo
        order.sudo().write({
            'shipping_mode': 'address',
            'branch_id': False,
        })

        return request.make_response(
            json.dumps({'ok': True, 'mode': 'address'}),
            headers=[('Content-Type','application/json; charset=utf-8')]
        )