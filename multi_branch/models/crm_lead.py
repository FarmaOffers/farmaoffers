# See LICENSE file for full copyright and licensing details.
"""CRM Lead Model."""


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Lead(models.Model):
    """CRM Lead Model."""

    _inherit = "crm.lead"

    branch_id = fields.Many2one(
        "multi.branch",
        string="Branch Name",
        default=lambda self: self.env.user.branch_id,
        ondelete="restrict",
    )

    @api.constrains("branch_id")
    def check_allow_branch(self):
        if self.branch_id and self.branch_id.id not in self.env.user.branch_ids.ids:
            raise ValidationError(_("Branch is not added in Allowed Branchs."))
