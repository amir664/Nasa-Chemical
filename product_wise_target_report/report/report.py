from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models
from datetime import datetime

class CustomReport(models.AbstractModel):
    _name = "report.product_wise_target_report.product_wise_target_reports"
    _description = "Product Wise Target Report"

    def _get_report_values(self, docids, data=None):
        customer = data['customer']
        product = data['product']
        start_date = data['start_date']
        end_date = data['end_date']

        others = {}

        cr = self._cr

        others= {
            'customer':customer,
            'product':product,
            'start_date':start_date,
            'end_date':end_date,
        }


        query = ("""
                    select 
                        pc.name as product_cat,
                        ctl.product_id as Code,
                        pt.name as Product ,
                        pt.list_price as Cost,
                        ctl.target as Target,
                        (ctl.target * pt.list_price) as total_cost,
                        ctl.sales_todate as Sales_date,
                        (ctl.sales_todate * pt.list_price) as sales_archive
                    from customer_target as ct
                        left join res_partner as res on ct.id= res.id
                        left join customer_target_line as ctl on ct.id = ctl.customer_target_id
                        left join product_product pp on ctl.product_id = pp.id
                        left join product_template pt on pp.product_tmpl_id = pt.id
                        left join product_category pc on pc.id = pt.categ_id 
                    
                """
                 
                )
        



        cr.execute(query)
        data = cr.dictfetchall()
        # raise UserError(str(data))

        return {
            'others' : others,
            'data' : data,
        }