from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'vendors.report'
    _description = 'Advance to Vendors Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    vendor_ids = fields.Many2many('res.partner', string = "Vendor")

    

    def print_report(self):

        vendor_ids = []
        if self.vendor_ids:
            for id in self.vendor_ids:
                vendor_ids.append(id.id)
        
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vendor_ids': vendor_ids,

            }

        return self.env.ref('vendors_report.vendors_report_pdf').with_context(landscape=True).report_action(self, data=data)