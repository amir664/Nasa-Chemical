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
        company_id = kwargs.get('company_id')

        domain = []
        if date_from:
            domain.append(('date_order', '>=', date_from))
        if date_to:
            domain.append(('date_order', '<=', date_to))
        if vendor_id:
            domain.append(('partner_id', '=', int(vendor_id)))
        if company_id:
            domain.append(('company_id', '=', int(company_id)))

        orders = request.env['purchase.order'].sudo().search(domain)
        vendors = {}

        for order in orders:
            if order.partner_id.name not in vendors:
                vendors[order.partner_id.name] = []
            
            for line in order.order_line:
                if item_wise and str(line.product_id.id) != item_wise:
                    continue  # Skip items that do not match the filter

                vendors[order.partner_id.name].append([
                    line.product_id.name,
                    line.product_qty,
                    line.product_uom.name,
                    line.price_total
                ])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Purchase Summary')

        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        cell_format = workbook.add_format({'border': 1})

        row = 0
        company_name = request.env['res.company'].sudo().browse(int(company_id)).name if company_id else "Company Name Not Found"
        sheet.merge_range(row, 0, row, 4, company_name, title_format)
        row += 1
        sheet.merge_range(row, 0, row, 4, 'Purchase Summary', title_format)
        row += 1
        sheet.write(row, 0, 'From Date: ' + (date_from or '____') + ' To: ' + (date_to or '____'))
        row += 2

        for vendor, lines in vendors.items():
            sheet.merge_range(row, 0, row, 4, vendor, header_format)
            row += 1
            sheet.write_row(row, 0, ['S #', 'Item', 'Qty', 'UOM', 'Amount'], header_format)
            row += 1
            for idx, line in enumerate(lines, start=1):
                sheet.write(row, 0, idx, cell_format)
                sheet.write_row(row, 1, line, cell_format)
                row += 1
            row += 1  # Space between vendors

        workbook.close()
        output.seek(0)

        return request.make_response(output.read(), [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename="purchase_summary.xlsx"')
        ])
