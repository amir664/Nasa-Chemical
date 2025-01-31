from odoo import _, api, fields, models


class POReportWizard(models.TransientModel):
    _name = 'monthly.report'
    _description = 'Purchase Order Month Wise Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    product_ids = fields.Many2many('product.template', string='Product')
    # warehouse_id = fields.Many2one('stock.warehouse', string = "Ware House")
    vendor_ids = fields.Many2many('res.partner', string='Vendor')
    
    

    def print_report(self):

        product_ids = []
        if self.product_ids:
            for id in self.product_ids:
                product_ids.append(id.id)
        
        vendor_ids = []
        if self.vendor_ids:
            for id in self.vendor_ids:
                vendor_ids.append(id.id)
    
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'product_ids': product_ids,
            'vendor_ids': vendor_ids
            
            }

        return self.env.ref('monthly_report.monthly_report_pdf').with_context(landscape=True).report_action(self, data=data)