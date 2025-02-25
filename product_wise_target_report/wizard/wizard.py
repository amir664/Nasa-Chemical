from odoo import _, fields, api, models

class CustomerTargetReport(models.TransientModel):
    _name = "product.wise.target.report"
    _description = "Product Wise Target Report"


    customer = fields.Many2one('res.partner', string = "Customer")
    product = fields.Many2one('product.product', string="Product")
    start_date = fields.Date(string = 'Start Date')
    end_date = fields.Date(string = 'End Date')

    def print_report(self):

        data = {
            'customer_id': self.customer.id if self.customer else False,
            'product_id': self.product.id if self.product else False,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
    
        return self.env.ref('product_wise_target_report.product_wise_target_report_pdf').with_context(landscape=False).report_action(self, data = data)