# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    whatsapp_number = fields.Char(string="Número de WhatsApp")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    whatsapp_number = fields.Char(
        string="Número de WhatsApp",
        related='website_id.whatsapp_number',
        readonly=False
    )

    has_whatsapp = fields.Boolean(
        string="Configurar WhatsApp",
        compute="_compute_has_whatsapp",
        inverse="_inverse_has_whatsapp"
    )

    @api.depends('website_id', 'whatsapp_number')
    def _compute_has_whatsapp(self):
        for record in self:
            record.has_whatsapp = bool(record.whatsapp_number)

    def _inverse_has_whatsapp(self):
        for record in self:
            if not record.has_whatsapp:
                record.whatsapp_number = ''