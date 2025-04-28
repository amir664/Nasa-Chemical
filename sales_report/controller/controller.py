# controllers/controller.py
from odoo import http
from odoo.http import request
import io
import xlsxwriter
import base64
from datetime import datetime

class SalesReportController(http.Controller):

    @http.route('/sales/report/excel', type='http', auth='user')
    def generate_sales_report(self, **kwargs):
        # Get Filters
        customer_id = kwargs.get('customer_id')
        city = kwargs.get('city')
        region = kwargs.get('region')
        salesperson_id = kwargs.get('salesperson_id')
        invoice_date_start = kwargs.get('invoice_date_start')
        invoice_date_end = kwargs.get('invoice_date_end')
        order_date_start = kwargs.get('order_date_start', '2023-01-01')
        order_date_end = kwargs.get('order_date_end', '2025-12-31')

        # Build SQL Query
        query = """
            SELECT
                rp.name AS customer,
                sol.name AS item,
                so.x_studio_city AS city,
                am.name AS inv_number,
                sol.product_uom_qty AS quantity,
                sol.price_unit AS unit_price,
                sol.price_subtotal AS sales,
                sol.price_subtotal AS cost_per_unit,
                (sol.price_subtotal * sol.product_uom_qty) AS total_cost
            FROM
                sale_order_line sol
            JOIN sale_order so ON sol.order_id = so.id
            LEFT JOIN account_move am ON am.invoice_origin = so.name
            JOIN res_partner rp ON so.partner_id = rp.id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            WHERE
                so.date_order BETWEEN %s AND %s
        """

        params = [order_date_start, order_date_end]

        if customer_id:
            query += " AND so.partner_id = %s"
            params.append(int(customer_id))
        if city:
            query += " AND so.x_studio_city = %s"
            params.append(city)
        if region:
            query += " AND so.x_studio_region = %s"  # Assuming region stored in x_studio_region
            params.append(region)
        if salesperson_id:
            query += " AND so.user_id = %s"
            params.append(int(salesperson_id))
        if invoice_date_start and invoice_date_end:
            query += " AND am.invoice_date BETWEEN %s AND %s"
            params.append(invoice_date_start)
            params.append(invoice_date_end)

        query += " ORDER BY so.date_order"

        # Execute Query
        request.env.cr.execute(query, tuple(params))
        results = request.env.cr.fetchall()

        # Create Excel File
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Sales Report')

        # Write Headers
        headers = ['Customer', 'Item', 'City', 'Invoice #', 'Quantity', 'Unit Price', 'Sales', 'Cost per Unit', 'Total Cost']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        # Write Data
        row = 1
        for line in results:
            for col, val in enumerate(line):
                sheet.write(row, col, val)
            row += 1

        workbook.close()
        output.seek(0)

        filename = f"Sales_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={filename}'),
            ]
        )
