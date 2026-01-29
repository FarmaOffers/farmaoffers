import threading
import logging
from odoo import models, _
from odoo.exceptions import ValidationError
from rootstack_ebi.document import ElectronicDocument

_logger = logging.getLogger(__name__)

lock_send_einvoice = threading.Lock()

class AccountMoveFEExtension(models.Model):
    _inherit = 'account.move'

    def action_send_electronic_invoice(self):
        """ Generate the electronic receipt and send it """
        with lock_send_einvoice:
            sequence_id = self.journal_id.sequence_id
            sequence = sequence_id.get_next_char(
                sequence_id.number_next_actual)
            if len(sequence) != 13:
                raise ValidationError(
                    _('the invoice number is not in the correct format'))
            serie = sequence[0:3]
            number = sequence[3:]
            self.ei_document_serie = serie
            self.ei_document_number = number
            edocument = ElectronicDocument()
            client = self.format_client_values()
            transaction = self.format_transaction_data()
            transaction.cliente = client
            if (self.move_type == 'out_refund' and self.reversed_entry_id) or self.debit_origin_id:
                """ Check if the document is a credit note or debit note"""
                listaDocsFiscalReferenciados = self.get_list_docs_referenced()
                transaction.listaDocsFiscalReferenciados = listaDocsFiscalReferenciados
            if self.journal_id.ei_document_type == '03':
                invoice_export_data = self.format_invoice_export_data()
                transaction.datosFacturaExportacion = invoice_export_data
            edocument.datosTransaccion = transaction
            items_list = self.format_items_data()
            edocument.listaItems = items_list
            totals = self.format_totals_data(items_data=items_list)
            payment = self.format_payment_data()
            totals.listaFormaPago = []
            totals.listaFormaPago.append(payment)
            edocument.totalesSubTotales = totals
            edocument.tipoSucursal = self.journal_id.branch_id.ei_branch_type
            edocument.codigoSucursalEmisor = self.journal_id.branch_id.ei_branch_code
            ebi_client = self.env.company.get_ebi_client()
            res = ebi_client.enviar(edocument)
            if res['codigo'] == '200':
                sequence_id._next_do()
                self.status_fe = '02'
                self.cufe_electronic_invoice = res['cufe']
                self.ei_qr = res['qr']
                return self.show_message()
            else:
                raise ValidationError(res['mensaje'])