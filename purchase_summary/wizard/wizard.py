from odoo import models, fields, api

class PSReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Many2one('product.product', string="Item(s)")

    
    # def print_report(self):
    #     """
    #     Generates the purchase order summary report based on the selected filters.
    #     """
    #     # purchase_orders = self.env['purchase.order']

    #     # item_wise = []
    #     # for po in purchase_orders:
    #     #     for line in po.order_line:
    #     #         if not self.item_wise or line.product_id in self.item_wise:
    #     #             item_wise.append(line.product_id.id)

    
    #     # data = {
    #     # 'items': item_wise,  # Sending only item IDs
    #     # }

    #     # Return report action with item names only
    #     return self.env.ref('summary_report.summary_report_pdf').with_context(landscape=True).report_action(
    #         self
    #     )
    def generate_excel_report(self):
            data = {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'vendor_id': self.vendor_id.id,
                'item_wise': self.item_wise
            }
            return {
                'type': 'ir.actions.act_url',
                'url': '/purchase_summary/excel_report?date_from={}&date_to={}&vendor_id={}&item_wise={}'.format(
                    self.date_from, self.date_to, self.vendor_id.id or '', self.item_wise.id or ''
                ),
                'target': 'new'
            }
