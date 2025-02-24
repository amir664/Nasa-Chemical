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
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        bold_left = workbook.add_format({'bold': True, 'align': 'left', 'border': 1})
        bold_right = workbook.add_format({'bold': True, 'align': 'right', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy', 'border': 1})
        bordered_format = workbook.add_format({'border': 1})  # Border for normal cells
        bold_bordered_format = workbook.add_format({'bold': True, 'border': 1})  # Bold with border

        # Merge and format title section
        worksheet.merge_range(0, 0, 0, 8, 'NASA CHEMICALS', bold_center)
        worksheet.merge_range(1, 0, 1, 8, '', bold_center)  # Empty spacer row
        worksheet.merge_range(2, 0, 2, 8, 'Bills Payable', bold_center)
        worksheet.merge_range(3, 0, 3, 8, 'Account Group : Sundry Creditors', bold_center)

        worksheet.merge_range(4, 0, 4, 4, f'From {date_from} to {date_to}', bold_left)
        worksheet.merge_range(4, 5, 4, 8, f'Bills Status as on : {date_to}', bold_right)

        # Column headers with borders
        headers = ['Vendor', 'PO', 'GRN', 'Invoice No', 'Invoice Date', 'Total Amount', 'Pending Amount', 'Due Date', 'Days']
        for col, header in enumerate(headers):
            worksheet.write(6, col, header, bold_center)

        # Prepare domain filters
        domain = []
        if date_from:
            domain.append(('date_approve', '>=', date_from))
        if date_to:
            domain.append(('date_approve', '<=', date_to))
        if vendor_ids:
            vendor_ids_list = [int(v) for v in vendor_ids.split(',')]
            domain.append(('partner_id', 'in', vendor_ids_list))
        if invoice:
            domain.append(('invoice_ids', 'in', int(invoice)))

        # Fetch purchase orders
        purchase_orders = request.env['purchase.order'].search(domain)
        row_idx = 7  # Start data after header row
        total_sum = 0
        pending_sum = 0

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
            payment_amount = sum(payments.mapped('amount'))
            pending_amount = total_amount - payment_amount

            # Accumulate sums
            total_sum += total_amount
            pending_sum += pending_amount

            # Write data to Excel with borders
            data = [vendor, po_name, grn, invoice, inv_date, total_amount, pending_amount, due_date, days]
            
            for col_idx, value in enumerate(data):
                if isinstance(value, datetime):
                    worksheet.write_datetime(row_idx, col_idx, value, date_format)
                else:
                    worksheet.write(row_idx, col_idx, value, bordered_format)
            row_idx += 1

        # Write totals row
        worksheet.write(row_idx, 4, "Total", bold_bordered_format)
        worksheet.write(row_idx, 5, total_sum, bold_bordered_format)
        worksheet.write(row_idx, 6, pending_sum, bold_bordered_format)

        workbook.close()
        output.seek(0)
        return request.make_response(output.read(),
                                     headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                              ('Content-Disposition', 'attachment; filename="{}"'.format(filename))])

