# farmaoffers_design/models/product_offers.py
from odoo import models, fields


class ProductOffers(models.Model):
    _name = 'product.offers'
    _description = "Special product offers"
    _order = "sequence, id"

    title = fields.Char(string="Title", size=60, required=True)
    description = fields.Text(string="Description")
    link = fields.Char(string="Link")
    image = fields.Binary(
        string='Image',
        help='Recommended image size: 256px x 256px.'
    )
    top = fields.Boolean(string="Top", default=True)
    type = fields.Selection(
        [
            ('product', 'Producto'),
            ('banner', 'Banner'),
        ],
        string='Tipo',
        required=True,
        default='banner',
    )
    product_id = fields.Many2one(
        'product.template',
        string='Producto',
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of this offer in lists/sliders.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
