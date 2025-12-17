from odoo import models, fields

class ClienttReviews(models.Model):
    _name = 'fo.client.review'
    _description = "Customer Reviews"

    title = fields.Char(string="Title", size=60)
    review = fields.Text(string="Review")
    active = fields.Boolean(default=True)