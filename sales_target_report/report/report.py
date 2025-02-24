from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.sales_target_report.sales_target_reports"
    _description = "Sales Target Report"

    def _get_report_values(self, docids, data=None):

        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        customer_ids = data['customer_ids']
        
        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
                'customer_ids': customer_ids,

            })
        
        if customer_ids != []:
            customer_ids_str = ','.join(map(str,customer_ids))
            
        query = (""" 
                    select 
                        res.name as customer_name,
                        res.region,
                        res.status,
                        res.town,
                        target.total_target,
                        target.total_sales_todate
                    from res_partner res
                        inner join customer_target target on res.id = target.customer
                        where 
                        target.start_date >= '%s' and target.end_date <= '%s'
                """

                % (date_from, date_to)) 


        if customer_ids:
            query += "AND res.id in (%s)" % customer_ids_str
        
        query += 'order by res.region'
        
        cr = self._cr
        cr.execute(query)
        result = cr.dictfetchall()

        

        return {
            'data': result,
            'other': other_details
        }