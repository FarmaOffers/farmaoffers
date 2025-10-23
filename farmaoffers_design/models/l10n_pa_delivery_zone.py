from odoo import models, fields

class DeliveryZone(models.Model):
    _name = "l10n.pa.delivery.zone"
    _description = "Delivery Zone"

    name = fields.Char(string="Nombre")
    code = fields.Char(string="Codigo")
    state_id = fields.Many2one("res.country.state", string="Estado / Provincia")
