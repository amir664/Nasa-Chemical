from odoo import models, fields, api

class PSReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Many2one('product.product', string="Item(s)")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    def generate_excel_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/purchase_summary/excel_report?date_from={}&date_to={}&vendor_id={}&item_wise={}&company_id={}'.format(
                self.date_from or '',
                self.date_to or '',
                self.vendor_id.id or '',
                self.item_wise.id or '',
                self.company_id.id or ''  
            ),
            'target': 'new'
        }
