from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models
from datetime import datetime

class CustomReport(models.AbstractModel):
    _name = "report.customer_target.customer_target_report"
    _description = "Customer Target Report"

    def _get_report_values(self, docids, data=None):
        customer = data['customer']
        start_date = data['start_date']
        end_date = data['end_date']
        sales_target = data['sales_target']
        current_sales = data['current_sales']


        other = {
            'customer': customer,
            'start_date': start_date,
            'end_date': end_date
        }

        cr = self._cr

        query = (f"""
                    SELECT 
                        ct.start_date, 
                        ct.end_date,
                        ctr.customer, 
                        rp.name AS customer_name,
                        ctl.sales_target, 
                        ctl.current_sales
                    FROM 
                        customer_target ct
                    LEFT JOIN 
                        customer_target_line AS ctl ON ct.id = ctl.customer_target_id
                    LEFT JOIN 
                        res_partner rp ON ctl.customer_target_id = rp.id
                    LEFT JOIN
                        customer_target_report AS ctr 

                 """)
        
        cr.execute(query)
        result = cr.dictfetchall()
        

        return {
            'data' : result,
        
        }