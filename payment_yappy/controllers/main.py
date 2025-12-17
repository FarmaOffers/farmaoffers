import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class YappyController(http.Controller):
    _secret_key = '5cKurIO61GWtpjhmhdoHjxC7gEbODGBx7rNzqqEUDfo='

    @http.route([
        '/payment/yappy/return',
        '/payment/yappy/fail'
    ], type='http', auth='public', csrf=False)
    def yappy_return(self, **post):
        """Handle Yappy return/fail callback in Odoo 18."""
        _logger.info('Beginning Yappy notification with post data %s',
                     pprint.pformat(post))
        request.env['payment.transaction'].sudo()._handle_notification_data('yappy', post)
        return werkzeug.utils.redirect('/payment/status')