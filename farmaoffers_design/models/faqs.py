from odoo import models, fields

class Faqs(models.Model):
    _name = 'fo.faqs'
    _description = "Frequently Asked Questions"

    title = fields.Char(string="Title", size=60)
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
