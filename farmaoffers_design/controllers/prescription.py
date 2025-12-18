import base64
import re

from odoo import http
from odoo.http import request


def validator(kw):
    """Validador de campos requeridos y formato básico."""
    errors = []

    required_fields = {
        'name': 'El nombre es requerido.',
        'lastname': 'El apellido es requerido.',
        'city': 'La ciudad es requerida.',
        'phone': 'El teléfono es requerido.',
        'email': 'El correo electrónico es requerido.',
        'message': 'El mensaje es requerido.',
    }

    for field, msg in required_fields.items():
        if not (kw.get(field) or '').strip():
            errors.append({'field': field, 'error': msg})

    name = (kw.get('name') or '').strip()
    if name and len(name) < 3:
        errors.append({
            'field': 'name',
            'error': 'El nombre debe tener al menos 3 caracteres.'
        })

    lastname = (kw.get('lastname') or '').strip()
    if lastname and len(lastname) < 3:
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


class Prescription(http.Controller):

    @http.route('/prescription', auth='public', type='http',
                methods=['GET', 'POST'], website=True, sitemap=False)
    def prescription(self, **kw):
        if request.httprequest.method == 'POST':

            upload = kw.get('upload', False)
            filename = upload.filename if upload else False
            file = upload.read() if upload else False

            errors = validator(kw)

            if not upload or not file:
                errors.append({
                    'field': 'upload',
                    'error': 'Debe adjuntar la prescripción en formato PDF.'
                })

            if upload and file and not file.startswith(b'%PDF-'):
                errors.append({
                    'field': 'upload',
                    'error': 'Ingrese un archivo PDF válido.'
                })

            if errors:
                kw['error'] = errors
                return request.render('farmaoffers_theme.prescription', kw)

            prescription = request.env['farmaoffers.prescription'].sudo().create({
                'name': kw.get('name'),
                'lastname': kw.get('lastname'),
                'city': kw.get('city'),
                'address': kw.get('address'),
                'phone': kw.get('phone'),
                'email': kw.get('email'),
                'message': kw.get('message'),
            })

            if upload and file:
                request.env['ir.attachment'].sudo().create({
                    'name': filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file),
                    'res_model': 'farmaoffers.prescription',
                    'res_id': prescription.id,
                    'res_field': 'file',
                    'mimetype': 'application/pdf',
                })

            render_values = {
                'title': 'Gracias!',
                'body': f"{prescription.name} estaremos contáctandole muy pronto",
                'back_button_text': 'Volver al inicio',
                'back_url': '/',
            }

            return request.render('farmaoffers_theme.thanks_page', render_values)

        return request.render('farmaoffers_theme.prescription')
