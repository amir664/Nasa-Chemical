from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.purchase_manualreport.purchase_manualreports"
    _description = "Purchase Report"


    def _get_report_values(self, docids, data=None):
        
        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        vendor_ids = data['vendor_ids']
        po_no = data['po_no']
        grn = data['grn']
        invoice_no = data['invoice_no']


        other_details.update({
                'from_date': date_from,
                'to_date': date_to,
                'product_ids': product_ids,
                'vendor_ids': vendor_ids,
                'po_no': po_no,
                'grn': grn,
                'invoice_no':invoice_no,
            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))


        cr = self._cr
        where_clauses = []
        params = []

        if date_from and date_to:
            where_clauses.append("po.date_order BETWEEN %s AND %s")
            params.extend([tuple(date_from), tuple(date_to)])

        if product_ids:
            where_clauses.append("pt.id IN %s")
            params.append(tuple(product_ids))  # Tuple for SQL IN clause

        if vendor_ids:
            where_clauses.append("rs.id IN %s")
            params.append(tuple(vendor_ids))
        # raise UserError(po_no)
        # if po_no:
        #     where_clauses.append("po.name = %s")
        #     params.append(tuple(po_no))

        # if grn:
        #     where_clauses.append("sp.name = %s")
        #     params.append(tuple(grn))

        # if invoice_no:
        #     where_clauses.append("am.name = %s")
        #     params.append(tuple(invoice_no))

        # Combine WHERE clauses
        where_clause = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = (f"""
                SELECT 
                    po.date_order AS Date,
                    rs.name as vendor,                    
                    pt.name ->> 'en_US' as item,
                    po.name AS PONo,
                    sp.name AS GRN,
                    am.name AS InvoiceNo,
                    sw.name as Location,
                    pol.product_qty AS qty,
                    mm.name ->> 'en_US'  AS Unit,
                    pol.price_unit AS price, 
                    pol.price_total AS amount
                FROM purchase_order_line pol 
                INNER JOIN purchase_order po ON po.id = pol.order_id
                inner JOIN product_product pp ON pp.id = pol.product_id
                inner JOIN product_template pt ON pt.id = pp.product_tmpl_id
                inner join res_partner rs on rs.id = po.partner_id
                Left JOIN stock_picking sp ON sp.origin = po.name   
                Left JOIN account_move am ON am.invoice_origin = po.name
                inner join stock_picking_type spt on spt.id = po.picking_type_id
                inner join stock_warehouse sw on sw.id = spt.warehouse_id
                inner join uom_uom mm on mm.id = pol.product_uom
                {where_clause}
                
                  

                order by po.name
                
                """
        
         )
        raise UserError(query)

        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
            'total_qty': sum(item['qty'] for item in data),
            'total_price': sum(item['price'] for item in data),
            
            'total_amount': sum(item['amount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }


        
