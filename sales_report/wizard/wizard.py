# wizards/sales_report_wizard.py
from odoo import models, fields
import urllib.parse

class SalesReportWizard(models.TransientModel):
    _name = 'sales.report.wizard'
    _description = 'Sales Report Wizard'

    customer_id = fields.Many2one('res.partner', string='Customer')
    city = fields.Char(string='City')
    region = fields.Char(string='Region')  # Assuming you save Region in sale_order
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    invoice_date_start = fields.Date(string='Invoice Start Date')
    invoice_date_end = fields.Date(string='Invoice End Date')
    order_date_start = fields.Date(string='Order Start Date', default=fields.Date.today)
    order_date_end = fields.Date(string='Order End Date')

    def action_generate_report(self):
        base_url = '/sales/report/excel?'

        params = {}

        if self.customer_id:
            params['customer_id'] = self.customer_id.id
        if self.city:
            params['city'] = self.city
        if self.region:
            params['region'] = self.region
        if self.salesperson_id:
            params['salesperson_id'] = self.salesperson_id.id
        if self.invoice_date_start and self.invoice_date_end:
            params['invoice_date_start'] = str(self.invoice_date_start)
            params['invoice_date_end'] = str(self.invoice_date_end)
        if self.order_date_start:
            params['order_date_start'] = str(self.order_date_start)
        if self.order_date_end:
            params['order_date_end'] = str(self.order_date_end)

        url = base_url + urllib.parse.urlencode(params)

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
