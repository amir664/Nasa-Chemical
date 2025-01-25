from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models
from datetime import datetime

class CustomReport(models.AbstractModel):
    _name = "report.customer_target_report.customer_target_reports"
    _description = "Customer Target Report"

    def _get_report_values(self, docids, data=None):
        customer = data['customer']
        start_date = data['start_date']
        end_date = data['end_date']
        # sales_target = data['sales_target']
        # current_sales = data['current_sales']


        other = {
            'customer': customer,
            'start_date': start_date,
            'end_date': end_date,
        }
        # raise UserError(str(other))


        # if customer_id != []:
        #     customer_id_str = ','.join(map(str,customer_id))

        cr = self._cr

        query = (f"""
                   
                    SELECT 
                        ct.start_date as start_date, 
                        ct.end_date as end_date,
                        rp.name AS customer_name,
                        ctl.sales_target, 
                        ctl.current_sales
                    FROM 
                        customer_target ct
                    LEFT JOIN 
                        customer_target_line AS ctl ON ct.id = ctl.customer_target_id
                    LEFT JOIN 
                        res_partner rp ON ctl.customer_target_id = rp.id
                 
                    
                 """)
        

        if other['customer'] and start_date != 'False' and end_date != 'False':
            query += " where rp.id = (%s) and ct.start_date between '%s' and '%s'" % (other['customer'],start_date,end_date)

        if start_date != 'False' and end_date != 'False':
            query += " ct.start_date >= '%s' and ct.start_date <= '%s'" % (start_date,end_date)



        cr.execute(query)
        result = cr.dictfetchall()

        raise UserError(str(result))        

        return {
            'data' : result,
        
        }