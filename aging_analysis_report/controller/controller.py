from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime, date

class AgingReportController(http.Controller):
    @http.route('/aging/excel_report', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_excel_report(self, date_from='', date_to='', vendor_ids=''):
        filename = "Aging_Report_{}.xlsx".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Aging Report')

        # Define formats
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        bordered_format = workbook.add_format({'border': 1})
        bold_bordered_format = workbook.add_format({'bold': True, 'border': 1})
        
        # Headers
        headers = [
            'Account', '( 0 - 30 ) Days', '( 31 - 60 ) Days', '( 61 - 90 ) Days',
            '( 91 - 120 ) Days', '( 121 - 150 ) Days', '(>=151) Days', 'Total Amt.'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold_center)
        
        # Prepare domain filters
        domain = []
        if date_from:
            domain.append(('date_approve', '>=', date_from))
        if date_to:
            domain.append(('date_approve', '<=', date_to))
        if vendor_ids:
            vendor_ids_list = [int(v) for v in vendor_ids.split(',')]
            domain.append(('partner_id', 'in', vendor_ids_list))
        
        # Fetch purchase orders
        purchase_orders = request.env['purchase.order'].search(domain)
        row_idx = 1

        for po in purchase_orders:
            vendor = po.partner_id.name
            due_date = po.due_date
            days = (date.today() - due_date).days if due_date else None
            amount = sum(po.invoice_ids.mapped('amount_total'))
            
            # Determine aging bucket
            aging_buckets = {'0-30': 0, '31-60': 0, '61-90': 0, '91-120': 0, '121-150': 0, '151+': 0}
            if days is not None:
                if days <= 30:
                    aging_buckets['0-30'] = amount
                elif days <= 60:
                    aging_buckets['31-60'] = amount
                elif days <= 90:
                    aging_buckets['61-90'] = amount
                elif days <= 120:
                    aging_buckets['91-120'] = amount
                elif days <= 150:
                    aging_buckets['121-150'] = amount
                else:
                    aging_buckets['151+'] = amount
            
            # Write row
            data = [vendor, aging_buckets['0-30'], aging_buckets['31-60'], aging_buckets['61-90'],
                    aging_buckets['91-120'], aging_buckets['121-150'], aging_buckets['151+'], amount]
            
            for col_idx, value in enumerate(data):
                worksheet.write(row_idx, col_idx, value, bordered_format)
            row_idx += 1
        
        workbook.close()
        output.seek(0)
        return request.make_response(output.read(),
                                     headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                              ('Content-Disposition', 'attachment; filename="{}"'.format(filename))])
