from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'aging.report'
    _description = 'Aging Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')

        

    def print_report(self):
        vendor_ids = ",".join(map(str, self.vendor_ids.ids)) if self.vendor_ids else ''
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/aging/excel_report?date_from={}&date_to={}'.format(
                self.date_from or '',
                self.date_to or ''
            ),
            'target': 'new'
        }
