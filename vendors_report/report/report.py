from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class CustomReport(models.AbstractModel):
    _name = "report.vendors_report.vendors_reports"
    _description = "Advance to Vendors Report"

    def _get_report_values(self, docids, data=None):
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        vendor_ids = data['vendor_ids']

        other_details.update({
            'date_from': date_from,
            'date_to': date_to,
            'vendor_ids': vendor_ids,
        })

        if vendor_ids:
            vendor_ids_str = ','.join(map(str, vendor_ids))

        cr = self._cr
        query = ("""
            SELECT 
                rs.name AS vendor,
                po.company_id AS id,
                po.date_order AS podate,
                po.name AS pono,
                SUM(pol.price_total) AS poamount,  -- Summing poamount
                am.date AS advdate,
                am.invoice_date_due AS duedate,
                apt.name ->> 'en_US' AS duedays,
                (am.invoice_date_due - po.date_order::DATE) AS duedays2
            FROM purchase_order po 
            INNER JOIN purchase_order_line pol ON pol.order_id = po.id 
            INNER JOIN res_partner rs ON rs.id = po.partner_id
            LEFT JOIN stock_picking sp ON sp.origin = po.name   
            LEFT JOIN account_move am ON am.invoice_origin = po.name
            LEFT JOIN account_payment_term apt ON apt.id = am.invoice_payment_term_id
            INNER JOIN stock_picking_type spt ON spt.id = po.picking_type_id
            INNER JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
            INNER JOIN uom_uom mm ON mm.id = pol.product_uom
            WHERE po.id IS NOT NULL
            and sp.state = 'done'
        """)

        if date_from and date_to:
    # Convert string dates to datetime objects
            date_from = datetime.strptime(date_from, "%Y-%m-%d") - timedelta(days=1)
            date_to = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            
            # Format back to string
            date_from = date_from.strftime("%Y-%m-%d")
            date_to = date_to.strftime("%Y-%m-%d")

            # Append the query condition
            query += " AND po.date_order BETWEEN '%s' AND '%s'" % (date_from, date_to)
        if vendor_ids:
            query += " AND rs.id IN (%s)" % (vendor_ids_str)

        query += """
            GROUP BY rs.name, po.company_id, po.date_order, po.name, am.date, am.invoice_date_due, apt.name
            ORDER BY po.name
        """
        raise UserError(query)
        cr.execute(query)
        data = cr.dictfetchall()

        # Compute `advamount` and `pendamount` in Python
        for record in data:
            po_name = record['pono']
            total_amount = record['poamount']

            # Fetch invoices linked to this PO
            bills = self.env['account.move'].search([('invoice_origin', '=', po_name)])
            # Fetch payments made against those invoices
            payments = self.env['account.payment'].search([('ref', 'in', bills.mapped('name'))])
            
            payment_amount = sum(payments.mapped('amount'))
            pending_amount = total_amount - payment_amount

            record['advamount'] = payment_amount
            record['pendamount'] = pending_amount

        # Compute totals
        totals = {
            'total_poamount': sum(item['poamount'] for item in data),
            'total_advamount': sum(item['advamount'] for item in data),
            'total_pendamount': sum(item['pendamount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals': totals,
            'other': other_details,
        }
