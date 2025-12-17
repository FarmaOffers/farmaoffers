# coding: utf-8
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('yappy', "Yappy")],
        ondelete={'yappy': 'set default'},
    )

    yappy_merchant_id = fields.Char(
        string="Yappy Merchant ID",
        required_if_provider='yappy',
        groups='base.group_system',
    )
    yappy_secret_key = fields.Char(
        string="Yappy Secret Key",
        required_if_provider='yappy',
        groups='base.group_system',
    )
    
    yappy_base_url = fields.Char(
        string="Custom Base URL (Opcional)",
        help="Si se llena, Yappy usará este dominio para callbacks."
    )

    def _get_default_payment_method_codes(self):
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'yappy':
            return default_codes
        return ['yappy']
    
    def _get_yappy_base_url(self):
        """Retorna la base URL para Yappy."""
        self.ensure_one()
        return self.yappy_base_url.strip() if self.yappy_base_url else self.get_base_url()