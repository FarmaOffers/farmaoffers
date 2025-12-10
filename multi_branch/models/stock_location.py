# See LICENSE file for full copyright and licensing details.
"""Stock Location model."""

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import odoo

MAJOR = getattr(odoo.release, "version_info", (18, 0, 0))[0]

class Location(models.Model):
    """Stock Location Inherited."""
    _inherit = "stock.location"

    branch_id = fields.Many2one("multi.branch", string="Branch Name")

    @api.onchange("branch_id")
    def _onchange_branch_id(self):
        for location in self:
            loc_id = location.location_id.id if location.location_id else False
            warehouse = self.env["stock.warehouse"].search(
                [("view_location_id", "=", loc_id)], limit=1
            )
            if warehouse and warehouse.branch_id and warehouse.branch_id != location.branch_id:
                raise UserError(_("You must select same branch on a location as assigned on a warehouse configuration."))

# ---- v14 heredaba stock.inventory / stock.inventory.line (eliminados en v15+)
if MAJOR < 15:
    class Inventory(models.Model):
        _inherit = "stock.inventory"
        branch_id = fields.Many2one("multi.branch", string="Branch Name")

    class InventoryLine(models.Model):
        _inherit = "stock.inventory.line"
        branch_id = fields.Many2one("multi.branch", string="Branch Name")
else:
    # En v15+ evita registrar clases sobre modelos que ya no existen
    class Inventory(models.Model):
        _inherit = "stock.inventory"
        _register = False

    class InventoryLine(models.Model):
        _inherit = "stock.inventory.line"
        _register = False