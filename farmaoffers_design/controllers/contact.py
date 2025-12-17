import re
from odoo import http, fields
from odoo.http import request


def _contact_validator(kw):
    errors = []

    required_fields = {
        'name': 'El nombre es requerido.',
        'company': 'La compañía es requerida.',
        'email': 'El correo electrónico es requerido.',
        'message': 'El mensaje es requerido.',
    }

    for field, msg in required_fields.items():
        if not (kw.get(field) or '').strip():
            errors.append({'field': field, 'error': msg})

    name = (kw.get('name') or '').strip()
    if name and len(name) < 3:
        errors.append({'field': 'name', 'error': 'El nombre debe tener al menos 3 caracteres.'})

    email = (kw.get('email') or '').strip()
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append({'field': 'email', 'error': 'Ingrese un correo electrónico válido.'})

    return errors


class FarmaoffersContactController(http.Controller):

    @http.route('/contactus', auth='public', type='http', methods=['GET', 'POST'], website=True, sitemap=False)
    def farmaoffers_contact(self, **kw):
        if request.httprequest.method == 'POST':
            errors = _contact_validator(kw)

            if errors:
                kw['error'] = errors
                return request.render('farmaoffers_theme.contact_us', kw)

            contact = request.env['fo.contactus'].sudo().create({
                'name': (kw.get('name') or '').strip(),
                'lastname': (kw.get('lastname') or '').strip(),
                'company': (kw.get('company') or '').strip(),
                'email': (kw.get('email') or '').strip(),
                'message': (kw.get('message') or '').strip(),
                'submission_date': fields.Datetime.now(),
            })

            render_values = {
                'title': 'Gracias!',
                'body': f"{contact.name} estaremos contáctandote muy pronto",
                'back_button_text': 'Volver al inicio',
                'back_url': '/',
            }
            return request.render('farmaoffers_theme.thanks_page', render_values)

        return request.render('farmaoffers_theme.contact_us')
