from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models

class CustomReport(models.AbstractModel):
    _name = "report.purchase_manualreport.purchase_manualreports"
    _description = "Purchase Report"

    def _get_report_values(self, docids, data=None):
        other_details = {}
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        product_ids = data.get('product_ids', [])
        vendor_ids = data.get('vendor_ids', [])
        po_no = data.get('po_no')
        grn = data.get('grn')
        invoice_no = data.get('invoice_no')

        other_details.update({
            'from_date': date_from,
            'to_date': date_to,
            'product_ids': product_ids,
            'vendor_ids': vendor_ids,
            'po_no': po_no,
            'grn': grn,
            'invoice_no': invoice_no,
        })

        cr = self._cr
        where_clauses = []
        params = []

        if date_from and date_to:
            where_clauses.append("po.date_order BETWEEN %s AND %s")
            params.extend([date_from, date_to])

        if product_ids:
            where_clauses.append("pt.id IN %s")
            params.append(tuple(product_ids))  # Tuple for SQL IN clause

        if vendor_ids:
            where_clauses.append("rs.id IN %s")
            params.append(tuple(vendor_ids))

        if po_no:
            where_clauses.append("po.name = %s")
            params.append(po_no)

        if grn:
            where_clauses.append("sp.name = %s")
            params.append(grn)

        if invoice_no:
            where_clauses.append("am.name = %s")
            params.append(invoice_no)

        # Combine WHERE clauses
        where_clause = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        query = f"""
            SELECT 
                po.date_order AS Date,
                rs.name AS vendor,                    
                pt.name ->> 'en_US' AS item,
                po.name AS PONo,
                sp.name AS GRN,
                am.name AS InvoiceNo,
                sw.name AS Location,
                pol.product_qty AS qty,
                mm.name ->> 'en_US' AS Unit,
                pol.price_unit AS price, 
                pol.price_total AS amount,
                COALESCE(pr.name, '') AS PurchaseRequest
            FROM purchase_order_line pol 
            INNER JOIN purchase_order po ON po.id = pol.order_id
            INNER JOIN product_product pp ON pp.id = pol.product_id
            INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
            INNER JOIN res_partner rs ON rs.id = po.partner_id
            LEFT JOIN stock_picking sp ON sp.origin = po.name   
            LEFT JOIN account_move am ON am.invoice_origin = po.name
            INNER JOIN stock_picking_type spt ON spt.id = po.picking_type_id
            INNER JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
            INNER JOIN uom_uom mm ON mm.id = pol.product_uom
            LEFT JOIN purchase_request_line prl ON prl.product_id = pol.product_id
            LEFT JOIN purchase_request pr ON pr.id = prl.request_id
            {where_clause}
            ORDER BY po.name

        """

        cr.execute(query, tuple(params))  # Execute with parameters
        data = cr.dictfetchall()

        totals = {
            'total_qty': sum(item['qty'] for item in data),
            'total_price': sum(item['price'] for item in data),
            'total_amount': sum(item['amount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals': totals,
            'other': other_details,
        }
