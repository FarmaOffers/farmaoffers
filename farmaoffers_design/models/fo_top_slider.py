from odoo import models, fields

class FoTopSlider(models.Model):
    _name = "fo.top.slider"
    _description = "FarmaOffers Top Slider"
    _order = "sequence"

    name = fields.Char(required=True)
    image = fields.Image("Image", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
