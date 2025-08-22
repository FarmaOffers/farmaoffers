# coding: utf-8

import logging
import json
import chardet
import os
from werkzeug import urls
from cryptography.fernet import Fernet

from odoo import api, fields, models, _
from odoo.tools.pycompat import to_text
from odoo.exceptions import ValidationError
from odoo.addons.payment_yappy.controllers.main import YappyController

_logger = logging.getLogger(__name__)


class AcquirerPaypal(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('yappy', 'Yappy')
    ], ondelete={'yappy': 'set default'})
    yappy_merchant_id = fields.Char(
        'Merchant ID', required_if_provider='yappy', groups='base.group_user')
    yappy_secret_key = fields.Char(
        'Secret Key', required_if_provider='yappy', groups='base.group_user')

    @api.model
    def _get_yappy_urls(self):
        from subprocess import check_output
        global form_data

        _logger.info("[YAPPY] _get_yappy_urls() called")
        _logger.info("[YAPPY] form_data keys: %s",
                     list(form_data.keys()) if isinstance(form_data, dict) else type(form_data))
        _logger.info("[YAPPY] acquirer state=%s merchant_id=%s base_url=%s",
                     getattr(self, 'state', None), getattr(self, 'yappy_merchant_id', None), self.get_base_url())

        # Encriptar referencia
        try:
            fernet = Fernet(YappyController._secret_key)
            encripted_reference = fernet.encrypt(form_data["reference"].encode()).decode()
            _logger.info("[YAPPY] reference encrypted OK (len=%d)", len(encripted_reference))
        except Exception as e:
            _logger.exception("[YAPPY] Error encrypting reference")
            raise

        # Armar payload
        data = {
            'environment': self.state,
            'merchant_id': self.yappy_merchant_id,
            'secret_key': self.yappy_secret_key,
            'payment': {
                'total': form_data['amount'],
                'subtotal': form_data['amount_untaxed'],
                'shipping': form_data['amount_delivery'],
                'discount': 0.00,
                'taxes': form_data['amount_tax'] or '0.00',
                'orderId': form_data['reference'],
                'successUrl': urls.url_join(self.get_base_url(),
                                            f'/payment/yappy/return?reference={encripted_reference}'),
                'failUrl': urls.url_join(self.get_base_url(),
                                         f'/payment/yappy/fail?fail=true&reference={encripted_reference}'),
                'tel': form_data['partner_phone'],
                'domain': self.get_base_url()
            }
        }
        _logger.info("[YAPPY] Payload para Node: %s", json.dumps(data))

        # Ejecutar Node
        node_script = os.path.expanduser('~') + '/node_sdk/dist/index.js'
        _logger.info("[YAPPY] Ejecutando Node: node %s", node_script)
        try:
            content = check_output(['node', node_script, json.dumps(data)])
            _logger.info("[YAPPY] Node output bytes len=%d", len(content) if content is not None else -1)
        except Exception as e:
            _logger.exception("[YAPPY] Error ejecutando Node script")
            raise

        # Decodificar salida
        try:
            enc_info = chardet.detect(content) or {}
            encoding = (enc_info.get('encoding') or '').lower()
            _logger.info("[YAPPY] chardet=%s | encoding=%s", enc_info, encoding)
            content = content.decode(encoding).encode('utf-8')
        except Exception as e:
            _logger.exception("[YAPPY] Error decodificando salida de Node")
            raise

        # Parsear JSON
        try:
            response = json.loads(to_text(content))
            _logger.info("[YAPPY] Respuesta de Node (dict keys): %s",
                         list(response.keys()) if isinstance(response, dict) else type(response))
            _logger.info("[YAPPY] Respuesta completa: %s", response)
        except Exception as e:
            _logger.exception("[YAPPY] Error parseando JSON de Node")
            raise

        # Evaluar respuesta
        if response['success']:
            _logger.info("[YAPPY] URL generada OK: %s", response['url'])
            return response['url']

        _logger.error("[YAPPY] Error desde Node | code=%s message=%s",
                      response.get('error', {}).get('code'),
                      response.get('error', {}).get('message'))
        raise ValidationError(f"{response['error']['code']} - {response['error']['message']}")

    def yappy_form_generate_values(self, values):
        _logger.info("[YAPPY] yappy_form_generate_values() called")
        _logger.info("[YAPPY] values recibidos: %s", values)
        global form_data
        self.ensure_one()
        form_data = values
        _logger.info("[YAPPY] form_data actualizado con reference=%s amount=%s",
                     values.get('reference'), values.get('amount'))
        return values

    def yappy_get_form_action_url(self):
        _logger.info("[YAPPY] yappy_get_form_action_url() called")
        self.ensure_one()
        url = self._get_yappy_urls()
        _logger.info("[YAPPY] URL devuelta por _get_yappy_urls(): %s", url)
        return url

    def get_form_action_url(self):
        _logger.info("[YAPPY] get_form_action_url() called")
        self.ensure_one()
        url = self.yappy_get_form_action_url()
        _logger.info("[YAPPY] URL final enviada al formulario: %s", url)
        return url


class TxAdyen(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _yappy_form_get_tx_from_data(self, data):
        fernet = Fernet(YappyController._secret_key)
        reference = fernet.decrypt(data.get('reference').encode()).decode()
        transaction = self.search([('reference', '=', reference)])
        return transaction

    def _yappy_form_validate(self, data):
        if (data.get('fail') == 'true'):
            error = 'No se pudo procesar el pago con Yappy'
            self._set_transaction_error(error)
            return self.write({
                'state_message': error
            })
        else:
            self._set_transaction_done()
        return True
