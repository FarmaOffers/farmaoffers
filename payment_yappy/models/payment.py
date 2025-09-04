# coding: utf-8
import logging
import json
import chardet
import os
from subprocess import check_output
from werkzeug import urls
from cryptography.fernet import Fernet

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.payment_yappy.controllers.main import YappyController

_logger = logging.getLogger(__name__)


class PaymentProviderYappy(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('yappy', 'Yappy')],
        ondelete={'yappy': 'set default'}
    )
    yappy_merchant_id = fields.Char(
        'Merchant ID', required_if_provider='yappy', groups='base.group_user')
    yappy_secret_key = fields.Char(
        'Secret Key', required_if_provider='yappy', groups='base.group_user')

    def _get_specific_rendering_values(self, processing_values):
        """Return redirect_url for Yappy."""
        if self.code != 'yappy':
            return super()._get_specific_rendering_values(processing_values)

        tx_sudo = processing_values['tx_sudo']
        fernet = Fernet(YappyController._secret_key)
        encrypted_ref = fernet.encrypt(tx_sudo.reference.encode()).decode()

        data = {
            'environment': self.state,
            'merchant_id': self.yappy_merchant_id,
            'secret_key': self.yappy_secret_key,
            'payment': {
                'total': tx_sudo.amount,
                'subtotal': tx_sudo.sale_order_ids[:1].amount_untaxed if tx_sudo.sale_order_ids else tx_sudo.amount,
                'shipping': getattr(tx_sudo.sale_order_ids[:1], 'amount_delivery', 0.0) if tx_sudo.sale_order_ids else 0.0,
                'discount': 0.00,
                'taxes': tx_sudo.sale_order_ids[:1].amount_tax if tx_sudo.sale_order_ids else 0.00,
                'orderId': tx_sudo.reference,
                'successUrl': urls.url_join(self.get_base_url(), f'/payment/yappy/return?reference={encrypted_ref}'),
                'failUrl': urls.url_join(self.get_base_url(), f'/payment/yappy/fail?fail=true&reference={encrypted_ref}'),
                'tel': tx_sudo.partner_id.phone or '',
                'domain': self.get_base_url(),
            }
        }

        _logger.info("DATA PARA GENERAR EL LINK DE YAPPY: %s", json.dumps(data))
        content = check_output(
            ['node', os.path.expanduser('~')+'/node_sdk/dist/index.js', json.dumps(data)])
        encoding = (chardet.detect(content)['encoding'] or 'utf-8').lower()
        response = json.loads(content.decode(encoding))

        _logger.info(response)
        if response.get('success'):
            return {'redirect_url': response['url']}
        raise ValidationError(
            f"{response['error']['code']} - {response['error']['message']}"
        )


class PaymentTransactionYappy(models.Model):
    _inherit = 'payment.transaction'

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Retrieve tx from reference."""
        if provider_code != 'yappy':
            return super()._get_tx_from_notification_data(provider_code, notification_data)

        fernet = Fernet(YappyController._secret_key)
        ref_enc = notification_data.get('reference')
        try:
            reference = fernet.decrypt(ref_enc.encode()).decode()
        except Exception:
            reference = ref_enc
        return self.search([('reference', '=', reference)], limit=1)

    def _process_notification_data(self, provider_code, notification_data):
        """Set tx state from notification."""
        if provider_code != 'yappy':
            return super()._process_notification_data(provider_code, notification_data)

        if notification_data.get('fail') == 'true':
            error = 'No se pudo procesar el pago con Yappy'
            self._set_error(error)
            return self.write({'state_message': error})
        else:
            self._set_done()
        return True