from odoo import models, fields, api

class Prescription(models.Model):
    _name = 'farmaoffers.prescription'
    _description = "Prescriptions."

    name = fields.Char(string="Name", size=60)
    lastname = fields.Char(string="Lastname", size=60)
    city = fields.Char(string="City", size=60)
    address = fields.Char(string="Address", size=60)
    phone = fields.Char(string="Phone", size=60)
    email = fields.Char(string="Email", size=60)
    message = fields.Text(string="Message")
    file = fields.Binary('File', help="Only PDFs", attachment=True)

    submission_date = fields.Datetime(string="Submission Date", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        now = fields.Datetime.now()
        for vals in vals_list:
            vals.setdefault('submission_date', now)
        return super().create(vals_list)
