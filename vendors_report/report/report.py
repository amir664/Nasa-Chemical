from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



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
        
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))

        cr = self._cr
        query = ("""
                    SELECT 
                            
                        rs.name as vendor,
                        po.company_id as id,
                        po.date_order AS podate,
                        po.name as pono,
                        pol.price_total AS poamount,
                        am.date as advdate,
                        
                        am.invoice_date_due as duedate,
                        apt.name ->> 'en_US' as duedays,
                        am.amount_total as advamount,
                        am.amount_residual_signed as pendamount,
                        po.company_id as id
                    
                        FROM purchase_order po 
                        INNER JOIN purchase_order_line pol ON pol.order_id = po.id 
                        inner join res_partner rs on rs.id = po.partner_id
                        Left JOIN stock_picking sp ON sp.origin = po.name   
                        Left JOIN account_move am ON am.invoice_origin = po.name
                        left join account_payment_term apt on apt.id = am.invoice_payment_term_id
                        inner join stock_picking_type spt on spt.id = po.picking_type_id
                        inner join stock_warehouse sw on sw.id = spt.warehouse_id
                        inner join uom_uom mm on mm.id = pol.product_uom

                    WHERE 
                        po.id is not null
                    
                    
                """
        
        )

        if date_from and date_to:
            query += "AND po.date_order BETWEEN '%s' AND '%s'" % (date_from, date_to)
        if vendor_ids:
            query += "AND rs.id in (%s)" % (vendor_ids_str)

        query += "order by po.name"

        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
                    'total_poamount': sum(item['poamount'] for item in data),
                    'total_advamount': sum(item['advamount'] if item['advamount'] is not None else 0 for item in data),
                    'total_pendamount': sum(item['pendamount'] if item['pendamount'] is not None else 0 for item in data),
        }


        # totals = {
        #     # 'total_poamount': sum(item['poamount'] for item in data),
        #     # 'total_advamount': sum(item['advamount'] for item in data or 0),
        #     # 'total_pendamount': sum(item['pendamount'] for item in data),
            
        # }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }


        
