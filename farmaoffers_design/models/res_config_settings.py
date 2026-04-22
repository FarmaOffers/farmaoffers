from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    whatsapp_number = fields.Char(
        string="Número de WhatsApp",
        related="website_id.whatsapp_number",
        readonly=False,
    )

    has_whatsapp = fields.Boolean(
        string="Configurar WhatsApp",
        compute="_compute_has_whatsapp",
        inverse="_inverse_has_whatsapp",
    )

    @api.depends("website_id", "whatsapp_number")
    def _compute_has_whatsapp(self):
        for record in self:
            record.has_whatsapp = bool(record.whatsapp_number)

    def _inverse_has_whatsapp(self):
        for record in self:
            if not record.has_whatsapp:
                record.whatsapp_number = ""
                
    branch_id = fields.Many2one(
        comodel_name='multi.branch',
        string='Sucursal',
        compute='_compute_branch_id',
        inverse='_inverse_branch_id',
    )

    @api.depends('pos_picking_type_id')
    def _compute_branch_id(self):
        for rec in self:
            picking_type = rec.pos_picking_type_id
            warehouse = picking_type.warehouse_id if picking_type else False
            rec.branch_id = warehouse.branch_id if warehouse else False

    def _inverse_branch_id(self):
        StockWarehouse = self.env['stock.warehouse']
        for rec in self:
            if not rec.branch_id:
                continue
            wh = StockWarehouse.search(
                [('branch_id', '=', rec.branch_id.id)],
                limit=1
            )
            if wh:
                rec.pos_picking_type_id = wh.pick_type_id
