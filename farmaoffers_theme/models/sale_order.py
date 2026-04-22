from odoo import models


class FarmaoffersSaleOrder(models.Model):
    _inherit = 'sale.order'

    def _check_cart_is_ready_to_be_paid(self):
        """En modo branch (retiro en tienda) no se requiere carrier_id."""
        if self.shipping_mode == 'branch':
            return
        return super()._check_cart_is_ready_to_be_paid()

    def _is_delivery_ready(self):
        """En modo branch el delivery siempre está listo."""
        if self.shipping_mode == 'branch':
            return True
        return super()._is_delivery_ready()