# from odoo.exceptions import UserError, AccessError
# from odoo import _, api, fields, models
# from datetime import datetime

# class CustomReport(models.AbstractModel):
#     _name = "report.customer_target.customer_target_report"
#     _description = "Customer Target Report"

#     def _get_report_values(self, docids, data=None):
#         customer = data['customer']
#         start_date = data['start_date']
#         end_date = data['end_date']

#         other = {
#             'customer': customer,
#             'start_date': start_date,
#             'end_date': end_date
#         }

#         cr = self._cr

#         query = (f"""
#                     SELECT 
#                     ct.start_date, 
#                     ct.end_date, 
#                     rp.name AS customer_name,
#                     ctl.sales_target, 
#                     ctl.current_sales
#                     FROM 
#                     customer_target ct
#                     LEFT JOIN 
#                     customer_target_line AS ctl ON ct.id = ctl.customer_target_id
#                     LEFT JOIN 
#                     sres_partner rp ON ctl.customer_target_id = rp.id

#                  """)
        
#         cr.execute(query)
#         result = cr.dictfetchall()
        

#         return {
#             'data' : result,
        
#         }