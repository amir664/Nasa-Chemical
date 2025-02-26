import io
import xlsxwriter
from datetime import datetime
from odoo import http
from odoo.http import request, content_disposition

class MrpProductionReportController(http.Controller):

    @http.route('/mrp_production_report', type='http', auth='user', website=True)
    def generate_report(self, date_from=None, date_to=None, product_id=None, **kwargs):
        """Generate an Excel report for MRP Production with headers."""

        domain = [('date_start', '>=', date_from), ('date_finished', '<=', date_to)]
        product_name = "All"
        if product_id:
            domain.append(('product_id', '=', int(product_id)))
            product = request.env['product.product'].browse(int(product_id))
            product_name = product.display_name

        productions = request.env['mrp.production'].search(domain)

        # Create an in-memory output file for the Excel workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('MRP Production Report')

        # Define formats
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        normal_format = workbook.add_format({'font_size': 12})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

        # Add report headings
        sheet.merge_range('A1:G1', "Production Summary Report", title_format)
        sheet.write('A2', "Print Out Date:", bold)
        sheet.write('B2', datetime.now().strftime('%d/%m/%Y %H:%M'), date_format)
        sheet.write('E2', "Nasa Chemicals (Pvt) Ltd", bold)

        sheet.write('A3', "Period:", bold)
        sheet.write('B3', f"{date_from} - {date_to}", normal_format)

        sheet.write('A4', "Item Group:", bold)
        sheet.write('B4', product_name, normal_format)

        # Define column headers
        headers = [ "Date","Batch #", "Item Name", "Qty", "W.O #", "Compl Date", "Mtr Cost"]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, bold)

        # Populate data rows
        row = 7
        for record in productions:
            valuation = request.env['stock.valuation.layer'].search([
                ('product_id', '=', record.product_id.id)
            ], limit=1, order='create_date DESC')

            sheet.write(row, 0, record.name)
            sheet.write(row, 1, str(record.date_start))
            sheet.write(row, 2, record.product_id.display_name)
            sheet.write(row, 3, record.product_qty)
            sheet.write(row, 4, record.lot_producing_id.name if record.lot_producing_id else '-')
            sheet.write(row, 5, str(record.date_finished))
            sheet.write(row, 6, valuation.value if valuation else 0.0)
            row += 1

        workbook.close()
        output.seek(0)

        # Return the Excel file as an HTTP response
        return request.make_response(output.getvalue(), [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', content_disposition('MRP_Production_Report.xlsx'))
        ])
