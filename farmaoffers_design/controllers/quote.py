import base64
import re

from odoo import http
from odoo.http import request

def validator(kw):
    errors = []

    required_fields = {
        'name': 'El nombre es requerido.',
        'lastname': 'El apellido es requerido.',
        'city': 'La ciudad es requerida.',
        'email': 'El correo electrónico es requerido.',
        'description': 'La descripción es requerida.',
    }

    for field, msg in required_fields.items():
        if not (kw.get(field) or '').strip():
            errors.append({'field': field, 'error': msg})

    if kw.get('name') and len(kw.get('name').strip()) < 3:
        errors.append({
            'field': 'name',
            'error': 'El nombre debe tener al menos 3 caracteres.'
        })

    if kw.get('lastname') and len(kw.get('lastname').strip()) < 3:
        errors.append({
            'field': 'lastname',
            'error': 'El apellido debe tener al menos 3 caracteres.'
        })

    email = (kw.get('email') or '').strip()
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append({
            'field': 'email',
            'error': 'Ingrese un correo electrónico válido.'
        })

    return errors

class QuoteController(http.Controller):

    @http.route('/quote', auth='public', type='http',
                methods=['GET', 'POST'], website=True, sitemap=False)
    def quote(self, **kw):

        if request.httprequest.method == 'POST':
            upload = kw.get('upload', False)
            filename = upload.filename if upload else False
            file = upload.read() if upload else False

            errors = validator(kw)

            if upload and file and not file.startswith(b'%PDF-'):
                errors.append({
                    'field': 'upload',
                    'error': 'Adjunte un archivo PDF válido.'
                })

            if errors:
                kw['error'] = errors
                return request.render('farmaoffers_theme.quote', kw)

            quote_rec = request.env['farmaoffers.quote'].sudo().create({
                'name': kw.get('name'),
                'lastname': kw.get('lastname'),
                'city': kw.get('city'),
                'address': kw.get('address'),
                'phone': kw.get('phone'),
                'email': kw.get('email'),
                'description': kw.get('description'),
            })

            if upload and file:
                request.env['ir.attachment'].sudo().create({
                    'name': filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file),
                    'res_model': 'farmaoffers.quote',
                    'res_id': quote_rec.id,
                    'res_field': 'file',
                    'mimetype': 'application/pdf',
                })

            return request.render('farmaoffers_theme.thanks_page', {
                'title': 'Gracias!',
                'body': f"{quote_rec.name}, hemos recibido su solicitud.",
                'back_button_text': 'Volver al inicio',
                'back_url': '/',
            })

        return request.render('farmaoffers_theme.quote')
