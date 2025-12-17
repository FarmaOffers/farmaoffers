from odoo import models, fields

class OurTips(models.Model):
    _name = 'fo.our.tips'
    _description = "Website Tips"

    text = fields.Char(string="Text", size=60)
    image = fields.Binary('Image', help='Image size must be 256px x 256px.')
    active = fields.Boolean(default=True)