from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class FarmaofferCustomerPortal(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = getattr(CustomerPortal, 'OPTIONAL_BILLING_FIELDS', []) + ['patient_program_ids']

    def details_form_validate(self, data):
        patient_program_values = []
        patient_program_ids = set()
        new_patient_program_ids = set()
        temp = {}

        for field in list(data.keys()):
            if field.startswith('program_name_') or field.startswith('affiliate_code_'):
                parts = field.split('_')
                if len(parts) >= 3:
                    try:
                        pid = int(parts[2])
                    except ValueError:
                        continue
                    if field.endswith('_new'):
                        new_patient_program_ids.add(pid)
                    else:
                        patient_program_ids.add(pid)
                    temp[field] = data.pop(field, None)

        for pid in patient_program_ids:
            name = temp.get(f'program_name_{pid}')
            code = temp.get(f'affiliate_code_{pid}')
            if (not name and not code) or (not name and code):
                continue
            patient_program_values.append(
                (1, pid, {
                    'program_name': name,
                    'affiliate_code': code,
                })
            )

        for pid in new_patient_program_ids:
            name = temp.get(f'program_name_{pid}_new')
            code = temp.get(f'affiliate_code_{pid}_new')
            if (not name and not code) or (not name and code):
                continue
            patient_program_values.append(
                (0, 0, {
                    'program_name': name,
                    'affiliate_code': code,
                })
            )

        res = super().details_form_validate(data)
        data.update({'patient_program_ids': patient_program_values})
        data.update(temp)
        return res