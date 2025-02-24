from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime

class AgingReportController(http.Controller):
    @http.route('/aging/excel_report', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_excel_report(self, date_from='', date_to='', vendor_ids='', invoice=''):
        filename = "Aging_Report_{}.xlsx".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Aging Report')

        # Define formats
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        bold_left = workbook.add_format({'bold': True, 'align': 'left'})
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})

        # Merge and format title section
        worksheet.merge_range('A1:N1', 'NASA CHEMICALS', bold_center)
        worksheet.merge_range('A2:N2', '', bold_center)
        worksheet.merge_range('A3:N3', 'Bills Payable', bold_center)
        worksheet.merge_range('A4:N4', 'Account Group : Sundry Creditors', bold_center)
        worksheet.merge_range('A5:G5', f'From {date_from} to {date_to}', bold_left)
        worksheet.merge_range('H5:N5', f'Bills Status as on : {date_to}', bold_right)

        # Column headers
        headers = ['From Date', 'To Date', 'Vendor', 'PO', 'GRN', 'Invoice No', 'Invoice Date', 'Total Amount',
                   'Due Date', 'Approval Date', 'Days', 'Payment Reference', 'Payment Date', 'Pending Amount']
        for col, header in enumerate(headers):
            worksheet.write(6, col, header, bold_center)

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
        row_idx = 7  # Start data after header row

        for po in purchase_orders:
            vendor = po.partner_id.name
            po_name = po.name
            grn = ', '.join(po.picking_ids.mapped('name'))
            invoice = ', '.join(po.invoice_ids.mapped('name'))
            inv_date = ', '.join([inv.invoice_date.strftime('%d-%m-%Y') for inv in po.invoice_ids if inv.invoice_date])
            total_amount = sum(po.invoice_ids.mapped('amount_total'))
            due_date = po.due_date.strftime('%d-%m-%Y') if po.due_date else ''
            approval_date = po.date_approve.strftime('%d-%m-%Y') if po.date_approve else ''
            days = (po.due_date - po.date_approve.date()).days if po.due_date and po.date_approve else ''

            # Fetch payments
            bills = request.env['account.move'].search([('invoice_origin', '=', po.name)])
            payments = request.env['account.payment'].search([('ref', 'in', bills.mapped('name'))])
            payment_ref = ', '.join(filter(None, payments.mapped('name')))
            payment_amount = sum(payments.mapped('amount'))
            payment_date = ', '.join([p.date.strftime('%d-%m-%Y') for p in payments if p.date])
            pending_amount = total_amount - payment_amount

            # Write data to Excel
            data = [date_from, date_to, vendor, po_name, grn, invoice, inv_date, total_amount, due_date,
                    approval_date, days, payment_ref, payment_date, pending_amount]
            
            for col_idx, value in enumerate(data):
                if isinstance(value, datetime):
                    worksheet.write_datetime(row_idx, col_idx, value, date_format)
                else:
                    worksheet.write(row_idx, col_idx, value)
            row_idx += 1

        workbook.close()
        output.seek(0)
        return request.make_response(output.read(),
                                     headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                              ('Content-Disposition', 'attachment; filename="{}"'.format(filename))])
