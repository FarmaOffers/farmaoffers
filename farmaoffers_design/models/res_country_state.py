from odoo import models, fields

class CountryState(models.Model):
    _inherit = 'res.country.state'

    zone_ids = fields.One2many(
        "l10n.pa.delivery.zone", "state_id", string="Zonas"
    )

    def get_website_sale_zones(self):
        return self.sudo().zone_ids
