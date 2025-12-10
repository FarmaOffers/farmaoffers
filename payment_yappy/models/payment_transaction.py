# coding: utf-8
import json
import logging
import os
from subprocess import check_output

import chardet
from cryptography.fernet import Fernet
from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_yappy.controllers.main import YappyController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'yappy':
            return res

        self.ensure_one()
        tx = self
        provider = self.provider_id

        fernet = Fernet(YappyController._secret_key)
        try:
            encrypted_ref = fernet.encrypt(tx.reference.encode()).decode()
        except Exception as e:
            _logger.exception("YAPPY encrypt error")
            raise ValidationError(_("Error encriptando referencia para Yappy: %s") % e)

        sale_order = tx.sale_order_ids[:1]
        total = tx.amount
        subtotal = sale_order.amount_untaxed if sale_order else tx.amount
        shipping = getattr(sale_order, 'amount_delivery', 0.0) if sale_order else 0.0
        taxes = sale_order.amount_tax if sale_order else 0.0

        base_url = self.provider_id._get_yappy_base_url()

        data = {
            'environment': provider.state,
            'merchant_id': provider.yappy_merchant_id,
            'secret_key': provider.yappy_secret_key,
            'payment': {
                'total': total,
                'subtotal': subtotal,
                'shipping': shipping,
                'discount': 0.00,
                'taxes': taxes or 0.00,
                'orderId': tx.reference,
                'successUrl': urls.url_join(
                    base_url,
                    f'/payment/yappy/return?reference={encrypted_ref}',
                ),
                'failUrl': urls.url_join(
                    base_url,
                    f'/payment/yappy/fail?fail=true&reference={encrypted_ref}',
                ),
                'tel': tx.partner_id.phone or '',
                'domain': base_url,
            }
        }

        _logger.info("YAPPY request data: %s", json.dumps(data, indent=2))

        module_root = os.path.dirname(os.path.dirname(__file__))
        node_script = os.path.join(module_root, 'node_sdk', 'dist', 'index.js')

        try:
            content = check_output(['node', node_script, json.dumps(data)])
        except Exception as e:
            _logger.exception("YAPPY node_sdk error")
            raise ValidationError(_("Error al generar el link de pago de Yappy: %s") % e)

        enc_info = chardet.detect(content) or {}
        encoding = (enc_info.get('encoding') or 'utf-8').lower()
        try:
            decoded = content.decode(encoding)
            response = json.loads(decoded)
        except Exception as e:
            _logger.exception("YAPPY invalid SDK response")
            raise ValidationError(_("Respuesta inválida del SDK de Yappy: %s") % e)

        _logger.info("YAPPY SDK response: %s", json.dumps(response, indent=2))

        if not response.get('success'):
            error = response.get('error') or {}
            code = error.get('code', 'UNKNOWN')
            msg = error.get('message', _('Error desconocido'))
            raise ValidationError(_("Yappy: %s - %s") % (code, msg))

        pay_url = response['url']
        
        if isinstance(pay_url, bytes):
          pay_url = pay_url.decode("utf-8")
          
        parsed_url = urls.url_parse(pay_url)
        
        def _to_str(x):
          if isinstance(x, bytes):
            return x.decode("utf-8")
          return x or ""
        
        scheme = _to_str(parsed_url.scheme)
        netloc = _to_str(parsed_url.netloc)
        path = _to_str(parsed_url.path)
        query = _to_str(parsed_url.query)
         
        api_url = f"{scheme}://{netloc}{path}"
        url_params = urls.url_decode(query) if query else {}
        

        rendering_values = {
            'api_url': api_url,
            "url_params": url_params,
        }
        _logger.info("YAPPY api_url: %s", pay_url)
        return rendering_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'yappy' or len(tx) == 1:
            return tx

        fernet = Fernet(YappyController._secret_key)
        ref_enc = notification_data.get('reference')
        if not ref_enc:
            raise ValidationError(_("Yappy: referencia ausente en la notificación."))

        try:
            reference = fernet.decrypt(ref_enc.encode()).decode()
        except Exception:
            _logger.warning("YAPPY: no se pudo desencriptar referencia, usando valor crudo")
            reference = ref_enc

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'yappy')], limit=1)
        if not tx:
            raise ValidationError(_("Yappy: no se encontró transacción con referencia %s.", reference))

        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'yappy':
            return

        fail = notification_data.get('fail')
        if fail == 'true':
            error = _('No se pudo procesar el pago con Yappy')
            _logger.warning("YAPPY: notificación de fallo para tx %s", self.reference)
            self._set_error(error)
            self.state_message = error
        else:
            _logger.info("YAPPY: notificación de éxito para tx %s", self.reference)
            self._set_done()
