from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    branch_id = fields.Many2one(
        comodel_name='multi.branch',
        string='Sucursal',
        compute='_compute_branch_id',
        inverse='_set_branch_id',
        store=True,
    )

    @api.depends('picking_type_id')
    def _compute_branch_id(self):
        """Calcula automáticamente el branch_id desde el picking_type"""
        for config in self:
            picking_type = config.picking_type_id
            warehouse = picking_type.warehouse_id if picking_type else False
            config.branch_id = warehouse.branch_id if warehouse else False

    def _set_branch_id(self):
        """Permite asignar manualmente un branch_id"""
        StockWarehouse = self.env['stock.warehouse']
        for config in self:
            if not config.branch_id:
                continue
            warehouses = StockWarehouse.search(
                [('branch_id', '=', config.branch_id.id)],
                limit=1
            )
            if warehouses:
                config.picking_type_id = warehouses.pick_type_id
