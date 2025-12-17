from odoo import models, fields

class BranchOffice(models.Model):
    _name = 'branch.office'
    _description = "Branch Offices"

    name = fields.Char(string="Name", size=60)
    description = fields.Text(string="Description")
    address = fields.Text(string="Address")