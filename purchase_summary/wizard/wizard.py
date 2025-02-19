from odoo import _, api, fields, models


class POReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Boolean(string="Item Wise")
    vendor_accounts_wise = fields.Boolean(string="Vendor Accounts Wise")
    vendor_group_wise = fields.Boolean(string="Vendor Group Wise")
    item_group_wise = fields.Boolean(string="Group of Item Wise")
    
    

    def print_report(self):

        # product_ids = []
        # if self.product_ids:
        #     for id in self.product_ids:
        #         product_ids.append(id.id)
        
        # vendor_ids = []
        # if self.vendor_ids:
        #     for id in self.vendor_ids:
        #         vendor_ids.append(id.id)
    
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            # 'product_ids': product_ids,
            # 'vendor_ids': vendor_ids
            
            }

        return self.env.ref('summary_report.summary_report_pdf').with_context(landscape=True).report_action(self, data=data)