# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'
  
    whatsapp_number = fields.Char(
        string="Número de WhatsApp",
        help="Número de WhatsApp en formato internacional, sin '+', ej: 50760000000",
    )
    def get_price_filter(self):
        """Return price filter sequence."""
        return self.env['price.filter'].sudo().search([], limit=1, order='sequence')

    def get_product_attributes(self):
        """Return all product attributes."""
        return self.env['product.attribute'].sudo().search([])

    def get_general_info_by_type(self, product, filter='general'):
        """Return general info or FAQ by product."""
        return self.env['product.general.info'].sudo().search([
            ('product_tmpl_id', '=', product),
            ('type', '=', filter)
        ])

    def get_products_with_same_compound(self, exception, filter=None):
        """Return products with the same compound, excluding the current one."""
        if not filter:
            return []
        return self.env['product.template'].sudo().search([
            ('id', '!=', exception),
            ('active_compound', '=', filter)
        ], limit=3)

    def get_product_offers(self, offer_type='banner'):
        """Return product offers filtered by type."""
        self.ensure_one()
        return self.env['product.offers'].sudo().search([
            ('type', '=', offer_type),
            ('active', '=', True),
        ], order="sequence, id")

    def get_branch_offices(self):
        """Return all branch offices."""
        return self.env['branch.office'].sudo().search([])

    def get_top_products(self, category=False):
        """Return top products ordered by sequence."""
        try:
            products = self.env['fo.top.product'].sudo().search(
                [], order='sequence')
            return products.mapped('product_tmpl_id')
        except Exception as e:
            _logger.error(f"Error in get_top_products: {e}")
            return []

    def get_top_sliders(self):
        """Return active top sliders."""
        return self.env['fo.top.slider'].sudo().search([('active', '=', True)])

    def get_main_categories(self):
        try:
            return self.env['product.public.category'].sudo().search([
                ('parent_id', '=', False),
                ('website_id', '!=', False)
            ])
        except Exception as e:
            _logger.error(f"Error obteniendo categorías principales: {e}")
            return []


class PriceFilter(models.Model):
    _name = 'price.filter'
    _description = "Price filter for website products"
    _order = 'sequence'

    price_under = fields.Float('Precio desde', digits=(12, 6), default=100)
    price_over = fields.Float('Precio hasta', digits=(12, 6), default=1000)
    price_range = fields.Float(
        'Rango de precios', digits=(12, 6), default=1000)
    sequence = fields.Integer('Sequence', default=10)

    @api.constrains('price_over')
    def _check_price_range(self):
        for record in self:
            if record.price_over < record.price_under:
                raise ValidationError(
                    f"El valor 'hasta' ({record.price_over}) debe ser mayor que 'desde' ({record.price_under})."
                )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    laboratory = fields.Char(string="Laboratorio", size=60)
    presentation = fields.Char(string="Presentación", size=60)
    active_compound = fields.Char(string="Compuesto activo", size=80)
    short_description = fields.Char(string="Descripción corta", size=80)
    ribbon_ids = fields.Many2many(
        'product.ribbon',
        'product_ribbon_rel', 'src_id', 'dest_id',
        string='Ribbons', help='Define your ribbons'
    )
    aditional_info_ids = fields.One2many(
        "product.aditional.info", "product_tmpl_id", string="Aditional information"
    )
    general_info_ids = fields.One2many(
        "product.general.info", "product_tmpl_id", string="General information"
    )

    def get_all_products_with_same_compound(self, compound):
        return self.search([('active_compound', '=', compound)])


class ResCompany(models.Model):
    _inherit = "res.company"

    disclaimer = fields.Text(string="Disclaimer")


class ProductAditionalInfo(models.Model):
    _name = 'product.aditional.info'
    _description = "Additional information for a product"

    description = fields.Text(string="Description")
    image = fields.Binary('Image', help='Image size must be 256px x 256px.')
    product_tmpl_id = fields.Many2one("product.template", string="Product")


class ProductGeneralInfo(models.Model):
    _name = 'product.general.info'
    _description = "General or FAQ information for a product"

    title = fields.Char(string="Title", size=60)
    description = fields.Text(string="Description")
    type = fields.Selection([
        ('general', 'General information'),
        ('faq', 'Frequent questions'),
        ('resume', 'Product resume')
    ], required=True, default='general')
    product_tmpl_id = fields.Many2one("product.template", string="Product")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    shipping_mode = fields.Selection([
        ('branch', 'Retirar en tienda'),
        ('address', 'Enviar a domicilio')
    ], string="Modo de entrega")
    branch_id = fields.Many2one("multi.branch", string="Branch")

    website_order_saving = fields.Float(
        compute='_compute_website_order_saving',
        string='Order Saving displayed on Website',
        help='Displayed savings for website orders.'
    )

    @api.depends('order_line')
    def _compute_website_order_saving(self):
        for order in self:
            full_price = sum(line.price_unit *
                             line.product_uom_qty for line in order.order_line)
            order.website_order_saving = full_price - order.amount_total


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipping_mode = fields.Selection([
        ('branch', 'Retirar en tienda'),
        ('address', 'Enviar a domicilio')
    ], string="Modo de entrega")
    branch_id = fields.Many2one("multi.branch", string="Branch")

class FarmaOffersContactUs(models.Model):
    _name = 'farmaoffers.contactus'
    _description = "Contact Form Submissions"

    name = fields.Char(string="Name", size=60)
    lastname = fields.Char(string="Lastname", size=60)
    company = fields.Char(string="Company", size=60)
    email = fields.Char(string="Email", size=60)
    message = fields.Text(string="Message")
