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
        bordered_format = workbook.add_format({'border': 1})
        bold_bordered_format = workbook.add_format({'bold': True, 'border': 1})

        # Merge and format title section
        worksheet.merge_range(0, 0, 0, 7, 'NASA CHEMICALS', bold_center)
        worksheet.merge_range(1, 0, 1, 7, '', bold_center)
        worksheet.merge_range(2, 0, 2, 7, 'Ageing Analysis ( Payables )', bold_center)
        worksheet.merge_range(3, 0, 3, 7, 'All Accounts', bold_center)
        worksheet.merge_range(4, 2, 4, 5, f'From {date_from} to {date_to}', bold_center)
        worksheet.merge_range(5, 2, 5, 5, f'Bills Status as on : {date_to}', bold_center)

        # Column headers
        headers = ['Account', '( 0 - 30 ) Days', '( 31 - 60 ) Days', '( 61 - 90 ) Days', '( 91 - 120 ) Days', '( 121 - 150 ) Days', '(>=151) Days', 'Total Amt.']
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

        # Fetch and group by vendor
        purchase_orders = request.env['purchase.order'].search(domain)
        grouped_data = {}
        for po in purchase_orders:
            vendor = po.partner_id.name
            due_date = po.due_date.date() if po.due_date else None
            days = (due_date - po.date_approve.date()).days if due_date and po.date_approve else 0
            total_amount = sum(po.invoice_ids.mapped('amount_total'))
            
            if vendor not in grouped_data:
                grouped_data[vendor] = {range: 0 for range in ['0-30', '31-60', '61-90', '91-120', '121-150', '151+']}
                grouped_data[vendor]['Total'] = 0
            
            if days <= 30:
                grouped_data[vendor]['0-30'] += total_amount
            elif days <= 60:
                grouped_data[vendor]['31-60'] += total_amount
            elif days <= 90:
                grouped_data[vendor]['61-90'] += total_amount
            elif days <= 120:
                grouped_data[vendor]['91-120'] += total_amount
            elif days <= 150:
                grouped_data[vendor]['121-150'] += total_amount
            else:
                grouped_data[vendor]['151+'] += total_amount
            
            grouped_data[vendor]['Total'] += total_amount

        # Write data rows
        row_idx = 7
        for vendor, amounts in grouped_data.items():
            worksheet.write(row_idx, 0, vendor, bordered_format)
            worksheet.write(row_idx, 1, amounts['0-30'], bordered_format)
            worksheet.write(row_idx, 2, amounts['31-60'], bordered_format)
            worksheet.write(row_idx, 3, amounts['61-90'], bordered_format)
            worksheet.write(row_idx, 4, amounts['91-120'], bordered_format)
            worksheet.write(row_idx, 5, amounts['121-150'], bordered_format)
            worksheet.write(row_idx, 6, amounts['151+'], bordered_format)
            worksheet.write(row_idx, 7, amounts['Total'], bold_bordered_format)
            row_idx += 1

        workbook.close()
        output.seek(0)
        return request.make_response(output.read(),
                                     headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                              ('Content-Disposition', 'attachment; filename="{}"'.format(filename))])