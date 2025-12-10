from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AccountMoveExtension(models.Model):
    _inherit = 'account.move'

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        if self.branch_id:
            _logger.info(f"Sucursal seleccionada: {self.branch_id.name}")
            if self.branch_id.journal_id:
                self.journal_id = self.branch_id.journal_id
                _logger.info(f"Diario contable asignado: {self.journal_id.name}")
            else:
                self.journal_id = False
                _logger.info("No se encontró un diario para la sucursal seleccionada.")
        else:
            self.journal_id = False
            _logger.info("No se seleccionó ninguna sucursal.")