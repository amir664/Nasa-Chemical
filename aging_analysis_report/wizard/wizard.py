from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'aging3.report'
    _description = 'Aging Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    vendor_ids = fields.Many2many('res.partner', string = "Vendor")
    invoice = fields.Many2one('account.move', string = "Invoice No.")
        

    def print_report(self):
        vendor_ids = ",".join(map(str, self.vendor_ids.ids)) if self.vendor_ids else ''
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/aging/excel_report?date_from={}&date_to={}&vendor_ids={}&invoice={}'.format(
                self.date_from or '',
                self.date_to or '',
                vendor_ids,
                self.invoice.id or ''
            ),
            'target': 'new'
        }
