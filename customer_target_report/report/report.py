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
        

        others = {}

        cr = self._cr

        others= {
            'start_date':start_date,
            'end_date':end_date,
            'customer':customer,
        }

        query = ("""
                   
                    SELECT 
            partner.name AS customer_name,
            --line.sales_target AS sales_target,
            line.current_sales AS current_sales,
            target.start_date AS start_date,
            target.end_date AS end_date
            FROM customer_target_line line
            JOIN customer_target target ON target.id = line.customer_target_id
            JOIN res_partner partner ON partner.id = line.customer
            
                    
                """
                % (customer, start_date, end_date) )
        
        cr.execute(query)
        data = cr.dictfetchall()

        return {
            'others' : others,
            'data' : data,
        }