from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models
from datetime import datetime


class CustomReport(models.AbstractModel):
    _name = "report.salesdetail_report.salesdetail_reports"
    _description = "Sales Detail Report"

    def _get_report_values(self, docids, data=None):

        other_details = {}
        to_date = data['to_date']
        from_date = data['from_date']
        partner_id = data['partner_id']
        category_id = data['category_id']
        partner_tag_id = data['partner_tag_id']
        city = data['city']
        branch = data['branch']
        area = data['area']


        other_details.update({
                'to_date': to_date,
                'from_date': from_date,
                'partner_id' : partner_id,
                'category_id' : category_id,
                'partner_tag_id' : partner_tag_id,
                'city': city,
                'branch': branch,
                'area': area
           })

        # if partner_id != []:
        #     partner_id_str = ','.join(map(str,partner_id))
        # if partner_tag_id != []:
        #     partner_tag_id_str = ','.join(map(str,partner_tag_id))
        # if category_id != []:
        #     category_id_str = ','.join(map(str,category_id))
        
        
        cr_1 = self._cr
        query = ("""

                    select distinct
                        so.date_order as date,
                        rp.name as customer,
                        so.user_id as broker,
                        rp.city as city,
                        am.name as invoice_no,
                        rpc.name ->> 'en_US' as sales_type,
                        sol.name as item,
                        sol.product_uom_qty as quantity,
                        um.name ->> 'en_US' as uom,
                        sol.price_unit as price,
                        sol.price_total as amount
                    from sale_order so
                    inner join res_partner rp on rp.id = so.partner_id
                    inner join sale_order_line sol on sol.order_id = so.id
                    inner join uom_uom um on um.id = sol.product_uom 
                    inner join account_move am on am.invoice_origin = so.name
                    left join res_partner_res_partner_category_rel rprpc on rprpc.partner_id = rp.id
                    left join res_partner_category rpc on rpc.id = rprpc.category_id
                    inner join product_template pt on pt.id = sol.product_id
                    where so.id is not null     
            """    
            )


        if partner_id:
            query += "and rp.id = %s"%(partner_id)

        if partner_tag_id:
            query += "and rprpc.category_id = %s"%(partner_tag_id)

        if category_id:
            query += "and pt.categ_id = %s"%(category_id)

        if from_date and to_date:
            query += "and so.date_order between '%s' and '%s'"%(from_date, to_date)

        if city:
            query += "and rp.city = '%s'"%(city)
        
        if branch:
            query += "and rp.city = '%s'"%(city)

        if area:
            query += "and rp.street = '%s'"%(city)



        cr_1.execute(query)
        data = cr_1.dictfetchall()

           
        return {
            'data': data,
            'other': other_details
        }
