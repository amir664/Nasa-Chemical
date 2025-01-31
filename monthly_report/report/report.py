from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.monthly_report.monthly_reports"
    _description = "Purchase Order Month Wise Report"


    def _get_report_values(self, docids, data=None):
        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        vendor_ids = data['vendor_ids']
        


        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
                'product_ids': product_ids,
                'vendor_ids': vendor_ids,

            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))

        cr = self._cr
        query = ("""
                 
                SELECT 
                    pt.name ->> 'en_US' as item,
                    mm.name ->> 'en_US' AS Unit,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 7 THEN pol.product_qty ELSE 0 END) AS qty_jul,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 7 THEN pol.price_subtotal ELSE 0 END) AS amount_jul,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 8 THEN pol.product_qty ELSE 0 END) AS qty_aug,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 8 THEN pol.price_subtotal ELSE 0 END) AS amount_aug,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 9 THEN pol.product_qty ELSE 0 END) AS qty_sep,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 9 THEN pol.price_subtotal ELSE 0 END) AS amount_sep,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 10 THEN pol.product_qty ELSE 0 END) AS qty_oct,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 10 THEN pol.price_subtotal ELSE 0 END) AS amount_oct,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 11 THEN pol.product_qty ELSE 0 END) AS qty_nov,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 11 THEN pol.price_subtotal ELSE 0 END) AS amount_nov,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 12 THEN pol.product_qty ELSE 0 END) AS qty_dec,
                    SUM(CASE WHEN EXTRACT(MONTH FROM po.date_order) = 12 THEN pol.price_subtotal ELSE 0 END) AS amount_dec,
                    SUM(pol.product_qty) AS qty,
                    SUM(pol.price_subtotal) AS amount,
                    max(po.company_id) as id

                FROM purchase_order po 
                INNER JOIN purchase_order_line pol ON pol.order_id = po.id
                INNER JOIN product_product pp ON pp.id = pol.product_id
                INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
                INNER JOIN res_partner rs ON rs.id = po.partner_id 
                LEFT JOIN stock_picking sp ON sp.origin = po.name   
                LEFT JOIN account_move am ON am.invoice_origin = po.name
                INNER JOIN stock_picking_type spt ON spt.id = po.picking_type_id
                INNER JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
                INNER JOIN uom_uom mm ON mm.id = pol.product_uom

                WHERE 
                    po.id is not null
                """)


        if date_from and date_to:
            query += "AND po.date_order BETWEEN '%s' AND '%s'" % (date_from, date_to)
        
        if product_ids:
            query += "AND pt.id in (%s)" % (product_ids_str)

        if vendor_ids:
            query += "AND rs.id in (%s)" % (vendor_ids_str)

        query += "GROUP BY pt.name, mm.name ORDER BY pt.name;" 

        #  % (date_from,date_to)
# ,category_ids,stock_location_id
        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
            'total_qty_jul': sum(item['qty_jul'] for item in data),
            'total_amount_jul': sum(item['amount_jul'] for item in data),
            
            'total_qty_aug': sum(item['qty_aug'] for item in data),
            'total_amount_aug': sum(item['amount_aug'] for item in data),
            
            'total_qty_sep': sum(item['qty_sep'] for item in data),
            'total_amount_sep': sum(item['amount_sep'] for item in data),
            
            'total_qty_oct': sum(item['qty_oct'] for item in data),
            'total_amount_oct': sum(item['amount_oct'] for item in data),
            
            'total_qty_nov': sum(item['qty_nov'] for item in data),
            'total_amount_nov': sum(item['amount_nov'] for item in data),
            
            'total_qty_dec': sum(item['qty_dec'] for item in data),
            'total_amount_dec': sum(item['amount_dec'] for item in data),
            
            'total_qty': sum(item['qty'] for item in data),
            'total_amount': sum(item['amount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }






                # SELECT 
                #     pt.name ->> 'en_US' as item,
                #     mm.name ->> 'en_US'  AS Unit,
                #     pol.product_qty AS qty,  
                #     pol.price_subtotal AS amount

                #     FROM purchase_order_line pol 
                #     INNER JOIN purchase_order po ON po.id = pol.order_id
                #     inner JOIN product_product pp ON pp.id = pol.product_id
                #     inner JOIN product_template pt ON pt.id = pp.product_tmpl_id
                #     inner join res_partner rs on rs.id = po.partner_id 
                #     Left JOIN stock_picking sp ON sp.origin = po.name   
                #     Left JOIN account_move am ON am.invoice_origin = po.name
                #     inner join stock_picking_type spt on spt.id = po.picking_type_id
                #     inner join stock_warehouse sw on sw.id = spt.warehouse_id
                #     inner join uom_uom mm on mm.id = pol.product_uom

                # WHERE 
                #     po.date_order BETWEEN '%s' AND '%s'
                #     AND pt.id in (%s)
                #     AND rs.id in (%s)

                # order by po.name
                
        
