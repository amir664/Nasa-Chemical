from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime

class PayableSummaryController(http.Controller):
    @http.route('/vendor_payable/excel_report', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_excel_report(self, date_from='', date_to=''):
        filename = "Payable_Summary_{}.xlsx".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Payable Summary')

        # Define formats
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        bold_left = workbook.add_format({'bold': True, 'align': 'left', 'border': 1})
        bold_right = workbook.add_format({'bold': True, 'align': 'right', 'border': 1})
        bordered_format = workbook.add_format({'border': 1})
        bold_bordered_format = workbook.add_format({'bold': True, 'border': 1})
        currency_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

        # Merge and format title section
        worksheet.merge_range(0, 0, 0, 1, 'NASA CHEMICALS', bold_center)
        worksheet.merge_range(2, 0, 2, 1, 'Payable Summary', bold_center)
        worksheet.merge_range(3, 0, 3, 1, 'Group : Accounts Payable', bold_center)
        worksheet.merge_range(4, 0, 4, 0, f'From {date_from} to {date_to}', bold_left)
        worksheet.merge_range(4, 1, 4, 1, f'Bills Status as on : {date_to}', bold_right)

        # Column headers
        headers = ['Account', 'Pending Amt.']
        for col, header in enumerate(headers):
            worksheet.write(6, col, header, bold_center)

        # Fetch data from account.move and payments
        domain = [('move_type', '=', 'in_invoice'), ('state', '=', 'posted')]
        if date_from:
            domain.append(('invoice_date', '>=', date_from))
        if date_to:
            domain.append(('invoice_date', '<=', date_to))

        invoices = request.env['account.move'].search(domain)
        vendor_data = {}
        
        for invoice in invoices:
            vendor_name = invoice.partner_id.name
            total_amount = invoice.amount_total
            payments = request.env['account.payment'].search([('ref', 'in', invoice.mapped('name'))])
            payment_amount = sum(payments.mapped('amount'))
            pending_amount = total_amount - payment_amount

            if vendor_name in vendor_data:
                vendor_data[vendor_name] += pending_amount
            else:
                vendor_data[vendor_name] = pending_amount

        # Write data to Excel
        row_idx = 7  # Start data after header row
        total_pending = 0
        
        for vendor, pending_amount in vendor_data.items():
            worksheet.write(row_idx, 0, vendor, bordered_format)
            worksheet.write(row_idx, 1, pending_amount, currency_format)
            total_pending += pending_amount
            row_idx += 1

        # Write totals row
        worksheet.write(row_idx, 0, "Totals", bold_bordered_format)
        worksheet.write(row_idx, 1, total_pending, currency_format)

        workbook.close()
        output.seek(0)
        return request.make_response(output.read(),
                                     headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                              ('Content-Disposition', 'attachment; filename="{}"'.format(filename))])
