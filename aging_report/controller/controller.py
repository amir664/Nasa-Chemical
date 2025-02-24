from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime

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
        headers = ['Vendor', 'PO', 'GRN', 'Invoice', 'Invoice Date', 'Total Amount', 'Due Date', 'Approval Date', 'Days', 'Payment Reference', 'Payment Amount', 'Payment Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)
        
        # Prepare domain filters
        domain = []
        if date_from:
            domain.append(('po.date_approve', '>=', date_from))
        if date_to:
            domain.append(('po.due_date', '<=', date_to))
        if vendor_ids:
            domain.append(('rp.id', 'in', [int(v) for v in vendor_ids.split(',')]))
        if invoice:
            domain.append(('am.id', '=', int(invoice)))
        
        # Execute query
        query = """
            SELECT rp.name AS Vendor, po.name AS PO, sp.name AS GRN, am.name AS Invoice,
                   am.invoice_date AS inv_date, am.amount_residual AS total_amount,
                   po.due_date, po.date_approve,
                   EXTRACT(DAY FROM po.due_date - po.date_approve)::INT+1 AS days,
                   ap.ref AS payment_reference, ap.amount AS payment_amount, ap.payment_date AS payment_date
            FROM purchase_order po
            LEFT JOIN res_partner rp ON po.partner_id = rp.id
            LEFT JOIN purchase_order_line pol ON po.id = pol.order_id
            LEFT JOIN stock_move sm ON pol.id = sm.purchase_line_id
            LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
            LEFT JOIN account_move_line aml ON pol.id = aml.purchase_line_id
            LEFT JOIN account_move am ON aml.move_id = am.id
            LEFT JOIN account_payment ap ON am.id = ap.move_id
            WHERE 1=1
        """
        
        # Apply filters
        if domain:
            for condition in domain:
                query += f" AND {condition[0]} {condition[1]} '{condition[2]}' "
        
        query += " GROUP BY rp.name, po.name, sp.name, am.name, am.invoice_date, am.amount_residual, po.due_date, po.date_approve, ap.ref, ap.amount, ap.payment_date "
        request.cr.execute(query)
        records = request.cr.fetchall()
        
        # Write data
        for row_idx, row in enumerate(records, start=1):
            for col_idx, value in enumerate(row):
                if isinstance(value, datetime):
                    worksheet.write_datetime(row_idx, col_idx, value, date_format)
                else:
                    worksheet.write(row_idx, col_idx, value)
        
        # Close workbook
        workbook.close()
        output.seek(0)
        
        # Return response
        return request.make_response(output.read(),
                                     headers=[
                                         ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                         ('Content-Disposition', 'attachment; filename="{}"'.format(filename))
                                     ])
