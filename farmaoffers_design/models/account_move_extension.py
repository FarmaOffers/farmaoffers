from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class AccountMoveExtension(models.Model):
    _inherit = 'account.move'

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        """
        Al cambiar la sucursal, asigna el diario contable correspondiente.
        Si la sucursal no tiene diario, deja journal_id vacío.
        """
        for move in self:
            if move.branch_id and getattr(move.branch_id, 'journal_id', False):
                move.journal_id = move.branch_id.journal_id
                _logger.info("Branch %s -> Journal %s", move.branch_id.display_name, move.journal_id.display_name)
            else:
                move.journal_id = False
                _logger.info("Branch vacío o sin journal -> journal_id=False")
