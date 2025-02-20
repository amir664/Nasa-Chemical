from odoo import _, api, fields, models
from odoo.exceptions import UserError, AccessError


class ReceivableWizard(models.TransientModel):
    _name = 'receivable.report'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    customer_ids = fields.Many2many('res.partner', string = "Customers")

    def print_report(self):
        customer_ids = []
        if self.partner_ids:
            for id in self.partner_ids:
                customer_ids.append(id.id)
                
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_ids': customer_ids,
        }

        return self.env.ref('sales_target_report.sales_target_report_pdf').with_context(landscape=True).report_action(self, data=data)
        
