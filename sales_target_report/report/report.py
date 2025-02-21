from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.sales_target_report.sales_target_reports"
    _description = "Custom Receivable Report"

    def _get_report_values(self, docids, data=None):

        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        partner_ids = data['partner_ids']
        
        other_details.update({
                'date_from': date_from,
                'date_to': date_to,
                'partner_ids': partner_ids,

            })
        
        if partner_ids != []:
            partner_ids_str = ','.join(map(str,partner_ids))
            
        query = (""" 
                    select 
                        rp.name as customer_name,
                        am.invoice_date as invoice_date,
                        am.name as invoice_no,
                        am.invoice_date_due as date_due,
                        am.amount_residual as amount

                    from account_move am
                        inner join res_partner rp on rp.id = am.partner_id
                        left join sale_order so on so.name = am.invoice_origin
                        left join account_analytic_account aca on aca.id = so.analytic_account_id

                        where 
                        am.create_date between '%s' and '%s'
                        and am.move_type = 'out_invoice'
                        
                """

                % (date_from, date_to)) 




        if partner_ids:
            query += "AND rp.id in (%s)" % partner_ids_str
        

        query += 'order by rp.name'
        
        cr = self._cr
        cr.execute(query)
        result = cr.dictfetchall()

        

        return {
            'data': result,
            'other': other_details
        }