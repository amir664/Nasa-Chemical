from odoo import _, fields, api, models

class CustomerTargetReport(models.TransientModel):
    _name = "customer.target.report"
    _description = "Customer Target Report"

    customer = fields.Many2one('res.partner', string = "Customer")
    start_date = fields.Date(string = 'Start Date')
    end_date = fields.Date(string = 'End Date')

    def print_report(self):

        data = {
            
            'start_date': self.start_date,
            'end_date': self.end_date,
            'customer': self.customer.id,
        }
    
        return self.env.ref('customer_target_report.customer_target_report_pdf').with_context(landscape=True).report_action(self, data = data)