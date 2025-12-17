from odoo import models, fields

class TopProduct(models.Model):
    _name = 'fo.top.product'
    _description = "Top products displayed on website"
    _order = 'sequence'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
        ondelete='cascade',
    )

    product_name = fields.Char(
        string="Name",
        related='product_tmpl_id.name',
        store=False,
        translate=False,
        readonly=True,
    )
    product_price = fields.Float(
        string="Price",
        related='product_tmpl_id.list_price',
        store=False,
        readonly=True,
    )
    product_image_1920 = fields.Binary(
        string="Image",
        related='product_tmpl_id.image_1920',
        store=False,
        readonly=True,
    )

    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
