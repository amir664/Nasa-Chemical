from odoo import models, fields, api
from odoo.http import Controller, route, request
import io
import xlsxwriter
from datetime import datetime

class PurchaseSummaryReportController(Controller):
    @route('/purchase_summary/excel_report', type='http', auth='user', methods=['GET'], csrf=False)
    def download_excel_report(self, **kwargs):
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        vendor_id = kwargs.get('vendor_id')
        item_wise = kwargs.get('item_wise')

        domain = []
        if date_from:
            domain.append(('date_order', '>=', date_from))
        if date_to:
            domain.append(('date_order', '<=', date_to))
        if vendor_id:
            domain.append(('partner_id', '=', int(vendor_id)))
        if item_wise:
            domain.append(('order_line.product_id', '=', int(item_wise)))

        orders = request.env['purchase.order'].sudo().search(domain)
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Purchase Summary')

        headers = ['Vendor', 'Purchase Order', 'Item', 'Quantity', 'UOM', 'Amount']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)
        
        row = 1
        for order in orders:
            for line in order.order_line:
                sheet.write(row, 0, order.partner_id.name)
                sheet.write(row, 1, order.name)
                sheet.write(row, 2, line.product_id.name)
                sheet.write(row, 3, line.product_qty)
                sheet.write(row, 4, line.product_uom.name)
                sheet.write(row, 5, line.price_total)
                row += 1

        workbook.close()
        output.seek(0)
        
        return request.make_response(output.read(), [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename="purchase_summary.xlsx"')
        ])
