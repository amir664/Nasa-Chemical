from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'aging.report'
    _description = 'Aging Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    vendor_ids = fields.Many2many('res.partner', string = "Vendor")
    invoice = fields.Many2one('account.move', string = "Invoice No.")
    

    def print_report(self):

        return {
            'type': 'ir.actions.act_url',
            'url': '/aging/excel_report?date_from={}&date_to={}&vendor_id={}&invoice={}'.format(
                self.date_from or '',
                self.date_to or '',
                self.vendor_id.id or '',
                self.item_wise.id or ''  
            ),
            'target': 'new'
        }