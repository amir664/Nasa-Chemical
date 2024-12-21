from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.pr_report.pr_reports"
    _description = "Party Wise Purchase Report"


    def _get_report_values(self, docids, data=None):
        
        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        party_ids = data['party_ids']
        po_no = data['po_no']
        grn = data['grn']
        invoice_no = data['invoice_no']


        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
                'product_ids': product_ids,
                'party_ids': party_ids,
                'po_no': po_no,
                'grn': grn,
                'invoice_no':invoice_no,
            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))
        if party_ids != []:
            party_ids_str = ','.join(map(str,party_ids))

        cr = self._cr
        query = ("""
                SELECT 
                    po.date_order AS Date,
                    po.company_id as id,                    
                    pt.name ->> 'en_US' as item,
                    po.origin as reqno,
                    po.name AS PONo,
                    sp.name AS GRN,
                    am.name AS InvoiceNo,

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

                WHERE po.id is not null
                """)
        
        if date_from and date_to:
            query += "AND po.date_order BETWEEN '%s' AND '%s'" % (date_from, date_to)
        
        if product_ids:
            query += "AND pt.id in (%s)" % (product_ids_str)

        if party_ids:
            query += "AND rs.id in (%s)" % (party_ids_str)
        
        if po_no:
            query += "AND po.name = '%s'" % (po_no)

        if grn:
            query += "AND sp.name = '%s'" % (grn)

        if invoice_no:
            query += "AND am.name = '%s'" % (invoice_no)

        

        query += "order by po.name"
        
        # % (date_from, date_to,product_ids_str, party_ids_str, po_no, grn, invoice_no) )

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


        
