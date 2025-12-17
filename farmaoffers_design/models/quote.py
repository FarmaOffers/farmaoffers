from odoo import models, fields, api

class Quote(models.Model):
    _name = 'fo.quote'
    _description = "Quotes"

    name = fields.Char(string="Name", size=60)
    lastname = fields.Char(string="Lastname", size=60)
    city = fields.Char(string="City", size=60)
    address = fields.Char(string="Address", size=60)
    phone = fields.Char(string="Phone", size=60)
    email = fields.Char(string="Email", size=60)
    description = fields.Text(string="Description")
    file = fields.Binary('File', help="Only PDFs", attachment=True)

    submission_date = fields.Datetime(string="Submission Date", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        now = fields.Datetime.now()
        for vals in vals_list:
            vals.setdefault('submission_date', now)
        return super().create(vals_list)
