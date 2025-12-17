# See LICENSE file for full copyright and licensing details.
"""Account and Payment Related Models."""

from odoo import api, fields, models


class AccountPayment(models.Model):
    """Account Payment."""

    _inherit = "account.payment"

    branch_id = fields.Many2one("multi.branch", string="Branch Name")

    @api.model
    def default_get(self, fields):
        """Overridden Method to update branch in Payment."""
        rec = super(AccountPayment, self).default_get(fields)
        active_ids = self._context.get("active_ids") or self._context.get("active_id")
        invoices = (
            self.env["account.move.line"]
            .browse(active_ids)
            .move_id.filtered(lambda move: move.is_invoice(include_receipts=True))
        )
        if invoices:
            rec["branch_id"] = (
                invoices[0].branch_id and invoices[0].branch_id.id or False
            )
        return rec


class AccountMoveLine(models.Model):
    """Account Move Line."""

    _inherit = "account.move.line"

    branch_id = fields.Many2one("multi.branch", string="Branch Name")


class AccountMove(models.Model):
    """Account Move."""

    _inherit = "account.move"

    branch_id = fields.Many2one(
        "multi.branch",
        string="Branch Name",
        default=lambda self: self.env.user.branch_id,
        ondelete="restrict",
    )

    @api.model_create_multi
    def create(self, vals):
        """Overridden create method to update the lines."""
        new_moves = super(AccountMove, self).create(vals)
        for move in new_moves:
            branch_id = move.branch_id.id if move.branch_id else False
            if branch_id:
                if move.line_ids:
                    move.line_ids.write({"branch_id": branch_id})
                if move.invoice_line_ids:
                    move.invoice_line_ids.write({"branch_id": branch_id})
        return new_moves

    def write(self, vals):
        """Overridden write method to update the lines."""
        res = super(AccountMove, self).write(vals)
        if vals.get("branch_id", False):
            for move in self:
                branch_id = move.branch_id.id if move.branch_id else False
                if branch_id:
                    if move.line_ids:
                        move.line_ids.write({"branch_id": branch_id})
                    if move.invoice_line_ids:
                        move.invoice_line_ids.write({"branch_id": branch_id})
        return res
