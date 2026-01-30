from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    branch_id = fields.Many2one(
        'multi.branch',
        string="Sucursal",
        help="Sucursal asociada al pedido de Punto de Venta."
    )

    @api.model
    def _process_order(self, order, existing_order):
        """
        Sobrescribe _process_order para asignar branch_id al pedido y a la factura.
        El branch_id se obtiene directamente desde pos.config.
        """
        _logger.info("Interceptando _process_order: Procesando pedido...")

        # Llamada correcta al método padre con la firma correcta
        order_id = super(PosOrder, self)._process_order(order, existing_order)

        # Obtener el recordset del pedido
        pos_order = self.browse(order_id)

        # Obtener branch_id desde la configuración de POS
        branch_id = pos_order.session_id.config_id.branch_id.id if pos_order.session_id.config_id.branch_id else False
        _logger.info(f"Branch ID obtenido desde POS Config: {branch_id}")

        if branch_id:
            # Asignar branch_id al pedido
            pos_order.write({'branch_id': branch_id})
            _logger.info(f"Branch ID {branch_id} asignado al pedido: {pos_order.name}")

            # Asignar branch_id a la factura si existe
            if pos_order.account_move:
                pos_order.account_move.write({'branch_id': branch_id})
                _logger.info(f"Branch ID {branch_id} asignado a la factura: {pos_order.account_move.name}")

        return order_id