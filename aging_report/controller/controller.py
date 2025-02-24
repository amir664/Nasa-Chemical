from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime
from odoo.exceptions import UserError, AccessError



class AgingReportController(http.Controller):
    @http.route('/aging/excel_report', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_excel_report(self, date_from='', date_to='', vendor_ids='', invoice=''):
        # Prepare filename
        filename = "Aging_Report_{}.xlsx".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

        # Create an in-memory output file
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Aging Report')

        # Define formats
        bold = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

        # Write headers
        headers = ['Vendor', 'PO', 'GRN', 'Invoice', 'Invoice Date', 'Total Amount',
                   'Due Date', 'Approval Date', 'Days', 'Payment Reference', 'Payment Amount', 'Payment Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Prepare domain filters
        domain = []
        if date_from:
            domain.append(('date_approve', '>=', date_from))
        if date_to:
            domain.append(('due_date', '<=', date_to))
        if vendor_ids:
            vendor_ids_list = [int(v) for v in vendor_ids.split(',')]
            domain.append(('partner_id', 'in', vendor_ids_list))
        if invoice:
            domain.append(('invoice_ids', 'in', int(invoice)))

        # Fetch purchase orders
        purchase_orders = request.env['purchase.order'].search(domain)

        row_idx = 1
        for po in purchase_orders:
            vendor = po.partner_id.name
            po_name = po.name
            grn = ', '.join(po.picking_ids.mapped('name'))
            invoice = ', '.join(po.invoice_ids.mapped('name'))
            inv_date = ', '.join([inv.invoice_date.strftime('%Y-%m-%d') for inv in po.invoice_ids if inv.invoice_date])
            total_amount = sum(po.invoice_ids.mapped('amount_residual'))
            due_date = po.due_date.strftime('%Y-%m-%d') if po.due_date else ''
            approval_date = po.date_approve.strftime('%Y-%m-%d') if po.date_approve else ''
            # days = (po.due_date - po.date_approve).days + 1 if po.due_date and po.date_approve else ''
            days = (po.due_date - po.date_approve.date()).days  if po.due_date and po.date_approve else ''


            # Fetch payments (Fixing KeyError issue)
            payments = request.env['account.payment'].search([('ref', 'in', po.invoice_ids.name)])
            payment_ref = 0#', '.join(payments.mapped('ref'))  # Fix: Use 'name' instead of 'communication'
            # payment_ref = ', '.join([ref for ref in payments.mapped('ref') if ref])
            # raise UserError(invoice)


            payment_amount = sum(payments.mapped('amount'))
            payment_date = ', '.join([p.payment_date.strftime('%Y-%m-%d') for p in payments if p.payment_date])

            # Write data to Excel
            data = [vendor, po_name, grn, invoice, inv_date, total_amount, due_date,
                    approval_date, days, payment_ref, payment_amount, payment_date]

            for col_idx, value in enumerate(data):
                if isinstance(value, datetime):
                    worksheet.write_datetime(row_idx, col_idx, value, date_format)
                else:
                    worksheet.write(row_idx, col_idx, value)

            row_idx += 1

        # Close workbook
        workbook.close()
        output.seek(0)

        # Return response
        return request.make_response(output.read(),
                                     headers=[
                                         ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                         ('Content-Disposition', 'attachment; filename="{}"'.format(filename))
                                     ])
