import io
import xlsxwriter
from odoo import http
from odoo.http import request, content_disposition

class MrpProductionReportController(http.Controller):

    @http.route('/mrp_production_report', type='http', auth='user', website=True)
    def generate_report(self, date_from=None, date_to=None, product_id=None, **kwargs):
        """Generate an Excel report for MRP Production."""

        domain = [('date_start', '>=', date_from), ('date_finished', '<=', date_to)]
        if product_id:
            domain.append(('product_id', '=', int(product_id)))

        productions = request.env['mrp.production'].search(domain)

        # Create an in-memory output file for the Excel workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('MRP Production Report')

        # Define header format
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})

        # Define column headers
        headers = ["Name", "Date Start", "Product", "Quantity", "Lot Producing", "Date Finished", "Valuation"]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        # Populate data rows
        row = 1
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
