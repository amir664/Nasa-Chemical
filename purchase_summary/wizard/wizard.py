from odoo import models, fields, api
from odoo.http import Controller, route, request
import io
import xlsxwriter
from datetime import datetime

class PSReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Many2one('product.product', string="Item(s)")

    def generate_excel_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vendor_id': self.vendor_id.id,
            'item_wise': self.item_wise.id
        }
        return {
            'type': 'ir.actions.act_url',
            'url': '/purchase_summary/excel_report?date_from={}&date_to={}&vendor_id={}&item_wise={}'.format(
                self.date_from, self.date_to, self.vendor_id.id or '', self.item_wise.id or ''
            ),
            'target': 'new'
        }