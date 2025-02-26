from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'totalvendor.report'
    _description = 'Aging Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')

        

    def print_report(self):
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/totalvendor/excel_report?date_from={}&date_to={}'.format(
                self.date_from or '',
                self.date_to or ''
            ),
            'target': 'new'
        }
