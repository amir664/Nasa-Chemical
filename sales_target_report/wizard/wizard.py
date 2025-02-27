from odoo import _, api, fields, models
from odoo.exceptions import UserError, AccessError


class SalesTargetWizard(models.TransientModel):
    _name = 'sales.target.report'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    region_ids = fields.Many2many('res.customer.region',string="Region")
    sub_region_ids = fields.Many2many('res.customer.region',string="Sub-Region")
    customer_ids = fields.Many2many('res.partner', string = "Customers")
    status = fields.Selection([('DISTRIBUTOR','DISTRIBUTOR'), ('DEALER', 'DEALER'), ('W.SELLER', 'W.SELLER'), ('WHOLESELLER', 'WHOLESELLER')]) 

    def print_report(self):
        customer_ids = []
        region_ids = []
        sub_region_ids = []
        if self.customer_ids:
            for id in self.customer_ids:
                customer_ids.append(id.id)
        if self.region_ids:
            for id in self.region_ids:
                region_ids.append(id.id)
        if self.sub_region_ids:
            for id in self.sub_region_ids:
                sub_region_ids.append(id.id)
                
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_ids': customer_ids,
            'region_ids': region_ids,
            'sub_region_ids': sub_region_ids,
            'status':self.status
        }

        return self.env.ref('sales_target_report.sales_target_report_pdf').with_context(landscape=True).report_action(self, data=data)
        
