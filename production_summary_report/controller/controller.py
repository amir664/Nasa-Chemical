import io
import xlsxwriter
from datetime import datetime
from odoo import http
from odoo.http import request, content_disposition

class MrpProductionReportController(http.Controller):

    @http.route('/mrp_production_report', type='http', auth='user', website=True)
    def generate_report(self, date_from=None, date_to=None, product_id=None, category_id=None, item_type='both', **kwargs):
        """Generate an Excel report for MRP Production with filters and advanced formatting."""

        domain = [('date_start', '>=', date_from), ('date_finished', '<=', date_to)]
        
        if product_id:
            domain.append(('product_id', '=', int(product_id)))

        if category_id:
            domain.append(('product_id.categ_id', '=', int(category_id)))

        # if item_type in ['fg', 'sfg']:
        #     domain.append(('product_id.default_code', 'ilike', f'{item_type.upper()}-'))
        if item_type == 'fg':
            domain.append(('product_id.default_code', '=like', 'FG-%'))
        elif item_type == 'sfg':
            domain.append(('product_id.default_code', '=like', 'SFG-%'))

        productions = request.env['mrp.production'].search(domain)

        # Create an in-memory output file for the Excel workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('MRP Production Report')

        # Define formats
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
        normal_format = workbook.add_format({'font_size': 12})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})

        # Merge for title
        sheet.merge_range('A1:I1', "Production Summary Report", title_format)
        sheet.write('A2', "Print Out Date:", bold)
        sheet.write('B2', datetime.now().strftime('%d/%m/%Y %H:%M'), date_format)
        sheet.write('E2', "Nasa Chemicals (Pvt) Ltd", bold)

        sheet.write('A3', "Period:", bold)
        sheet.write('B3', f"{date_from} - {date_to}", normal_format)

        sheet.write('A4', "Item Group:", bold)
        sheet.write('B4', "Finished Goods" if item_type == 'fg' else "Semi-Finished Goods" if item_type == 'sfg' else "Both", normal_format)

        # Define column headers
        headers = ["MO", "MO Start Date", "MO Completion Date", "Item Name", "Batch / Lot", "Lot Creation Date", "Qty", "Mtr Cost"]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, bold)

        # Populate data rows
        row = 7
        for record in productions:
            valuation = request.env['stock.valuation.layer'].search([
                ('product_id', '=', record.product_id.id)
            ], limit=1, order='create_date DESC')

            sheet.write(row, 0, record.name)  # MO
            sheet.write(row, 1, record.date_start, date_format)  # MO Start Date
            sheet.write(row, 2, record.date_finished, date_format)  # MO Completion Date
            sheet.write(row, 3, record.product_id.display_name)  # Item Name
            sheet.write(row, 4, record.lot_producing_id.name if record.lot_producing_id else '-')  # Batch/Lot
            sheet.write(row, 5, record.lot_producing_id.create_date if record.lot_producing_id else '-', date_format)  # Lot Creation Date
            sheet.write(row, 6, record.product_qty)  # Qty
            # sheet.write(row, 7, record.origin if record.origin else '-')  # W.O #
            sheet.write(row, 7, valuation.value if valuation else 0.0, currency_format)  # Mtr Cost
            row += 1

        # Auto-fit columns
        sheet.set_column('A:I', 18)

        workbook.close()
        output.seek(0)

        # Return the Excel file as an HTTP response
        return request.make_response(output.getvalue(), [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', content_disposition('MRP_Production_Report.xlsx'))
        ])
