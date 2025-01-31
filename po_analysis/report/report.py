from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.po_analysis.po_analysiss"
    _description = "Purchase Order Analysis Report"


    def _get_report_values(self, docids, data=None):
        
    

        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        warehouse_id = data['warehouse_id']
        vendor_ids = data['vendor_ids']
        po_no = data['po_no']
        grn = data['grn']


        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
                'product_ids': product_ids,
                'warehouse_id': warehouse_id,
                'vendor_ids': vendor_ids,
                'po_no': po_no,
                'grn': grn,
            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))

        cr = self._cr
        query = ("""
                SELECT 
                    pt.name ->> 'en_US' as item,
                    po.company_id as id,
                    mm.name ->> 'en_US'  AS Unit,
                    pol.product_qty AS qty,  
                    pol.price_subtotal AS amount

                    FROM purchase_order po 
                    INNER JOIN purchase_order_line pol ON pol.order_id = po.id
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

        if vendor_ids:
            query += "AND rs.id in (%s)" % (vendor_ids_str)
        
        if warehouse_id:
            query += "AND spt.warehouse_id = %s" % (warehouse_id)

        if po_no:
            query += "AND po.name = '%s'" % (po_no)

        if grn:
            query += "AND sp.name = '%s'" % (grn)

        query += "order by po.name"

        
        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
            'total_qty': sum(item['qty'] for item in data),
            'total_amount': sum(item['amount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }


        
