from odoo import models, fields, api

class ContactUs(models.Model):
    _name = 'fo.contactus'
    _description = "Contact Us"

    name = fields.Char(string="Name", required=True)
    lastname = fields.Char(string="Lastname")
    company = fields.Char(string="Company", required=True)
    email = fields.Char(string="Email", required=True)
    message = fields.Text(string="Message", required=True)

    submission_date = fields.Datetime(string="Submission Date", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        now = fields.Datetime.now()
        for vals in vals_list:
            vals.setdefault('submission_date', now)
        return super().create(vals_list)
