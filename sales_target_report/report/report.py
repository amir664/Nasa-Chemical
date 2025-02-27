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
        region_ids = data['region_ids']
        sub_region_ids = data['sub_region_ids']
        status = data['status']
        
        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
            })
        
        if customer_ids != []:
            customer_ids_str = ','.join(map(str,customer_ids))
        if region_ids != []:
            region_ids_str = ','.join(map(str,region_ids))
        if sub_region_ids != []:
            sub_region_ids_str = ','.join(map(str,sub_region_ids))
            
        query = (""" 
                    select 
                        res.name as customer_name,
                        res.region_id,
                        res.sub_region_id,
                        res.status,
                        res.town,
                        target.total_target,
                        target.id,
                        (select amount_total from sale_order where partner_id = res.id and state not in ('cancel','draft')) as sales_achieved
                        
                    from res_partner res
                        inner join customer_target target on res.id = target.customer
                        where 
                        target.start_date >= '%s' and target.end_date <= '%s'
                """

                % (date_from, date_to)) 


        if customer_ids:
            query += "AND res.id in (%s)" % customer_ids_str
        if region_ids:
            query += "AND res.region_id in (%s)" % region_ids_str
        if sub_region_ids:
            query += "AND res.sub_region_id in (%s)" % sub_region_ids_str
        if status:
            query += "AND res.status = (%s)" % status
                
        query += "order by region_id,sub_region_id"
        cr = self._cr
        cr.execute(query)
        result = cr.dictfetchall()

        

        return {
            'data': result,
            'other': other_details
        }