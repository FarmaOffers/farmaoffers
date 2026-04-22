# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.website_sale.controllers.main import WebsiteSale
import base64
import logging
import re
import werkzeug
from odoo.addons.web.controllers.home import Home
from odoo.addons.theme_grocery.controllers.controllers import website_sale as ThemeGroceryWebsiteSale


# Make a regular expression
# for validating an Email
regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#regexName =r'/^[\w\s]+$/'

_logger = logging.getLogger(__name__)

class SignUpFO(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        errors = validator(qcontext)
        if len(errors) > 0:
            qcontext["error"] = [qcontext["error"]] + \
                errors if 'error' in qcontext else errors

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref(
                        'auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _(
                        "Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        errors = validator(qcontext, qcontext.get('token'))
        if len(errors) > 0:
            qcontext["error2"] = errors

        if 'error' not in qcontext and 'error2' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return self.web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    request.env['res.users'].sudo().reset_password(login)
                    qcontext['message'] = _(
                        "An email has been sent with credentials to reset your password")
            except UserError as e:
                qcontext['error'] = e.args[0]
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    def _signup_with_values(self, token, values):
        context = self.get_auth_signup_qcontext()
        values.update({'street': context.get('address')})
        values.update({'phone': context.get('phone')})
        super(SignUpFO, self)._signup_with_values(token, values)

    @http.route(['/products/same-compounds'], type='json', website=True, auth='public', Sitemap=False)
    def get_all_products_with_same_compound(self, exception, compound=None, limit=None):
        products = http.request.env['product.template'].search(
            [('id', '!=', exception), ('active_compound', '=', compound)], limit=limit)
        jsonProducts = []
        for product in products:
            jsonProducts.append(
                {"id": product.id, "name": product.name, "website_url": product.website_url})

        return jsonProducts
    

def validator(data, onlypaswords=False):
    errors = []
    for key in data.keys():
        if not onlypaswords and (key == 'name' or key == 'lastname'):
            if len(data[key]) < 5:
                errors.append(
                    {'field': key, 'error': f'El campo {key} debe tener más de 4 caracteres.'})
            if not re.match(r'[a-zA-Z +\s]+$', data[key]):
                errors.append(
                    {'field': key, 'error': f'El campo {key} debe contener solo letras.'})

        if not onlypaswords and (key == 'email' or key == 'login'):
            if not (re.fullmatch(regexEmail, data[key])):
                errors.append(
                    {'field': key, 'error': f'El campo {key} debe ser un correo válido.'})

        if not onlypaswords and (key == 'phone'):
            if not data[key].isdigit():
                errors.append(
                    {'field': key, 'error': f'El campo {key} debe ser śolo numéros.'})

            if len(data[key]) != 8 and len(data[key]) != 7:
                errors.append(
                    {'field': key, 'error': f'El campo {key} debe tener 7 u 8 dígitos.'})

        if key == 'password':
            SpecialSym = ['$', '@', '#', '%']
            val = True

            if len(data[key]) < 6:
                val = False

            if not any(char.isdigit() for char in data[key]):
                val = False

            if not any(char.isupper() for char in data[key]):
                val = False

            if not any(char.islower() for char in data[key]):
                val = False

            if not any(char in SpecialSym for char in data[key]):
                val = False
            if not val:
                errors.append(
                    {'field': key, 'error': f'La contraseña debe contener 6 o más dígitos, debe contener al menos 1 mayúscula, 1 minúscula, 1 número y 1 símbolo ($, @, #, %).'})

    return errors

class HomeRedirect(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        if request.session.uid:
            return request.redirect('/')
        return super().web_login(redirect=redirect, **kw)
    
from odoo.http import request, route
from odoo.addons.theme_grocery.controllers.controllers import website_sale as ThemeGroceryWebsiteSale
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.tools import lazy

class WebsiteSalePriceFix(ThemeGroceryWebsiteSale):

    def _safe_float(self, val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return False

    @route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=ThemeGroceryWebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):

        res = super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post
        )

        min_price = self._safe_float(request.params.get('min_price'))
        max_price = self._safe_float(request.params.get('max_price'))
        res.qcontext['min_price'] = min_price if min_price is not False else res.qcontext.get('available_min_price')
        res.qcontext['max_price'] = max_price if max_price is not False else res.qcontext.get('available_max_price')

        products = res.qcontext.get('products')
        if products:
            filtered_products = products

            if min_price is not False:
                filtered_products = filtered_products.filtered(lambda p: p.list_price >= min_price)

            if max_price is not False:
                filtered_products = filtered_products.filtered(lambda p: p.list_price <= max_price)

            res.qcontext['products'] = filtered_products
            res.qcontext['search_product'] = filtered_products
            res.qcontext['search_count'] = len(filtered_products)

            ppg = res.qcontext.get('ppg') or ppg or 20
            ppr = res.qcontext.get('ppr') or 4

            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(filtered_products, ppg, ppr)
            )

        return res