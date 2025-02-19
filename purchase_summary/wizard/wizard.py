from odoo import models, fields, api

class PSReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Many2many('product.product.id', string="Item(s)")

    
    def print_report(self):
        """
        Generates the purchase order summary report based on the selected filters.
        """
        # purchase_orders = self.env['purchase.order']

        # item_ids = []
        # for po in purchase_orders:
        #     for line in po.order_line:
        #         if not self.item_wise or line.product_id in self.item_wise:
        #             item_ids.append(line.product_id.id)

    
        # data = {
        # 'items': item_ids,  # Sending only item IDs
        # }

        # Return report action with item names only
        return self.env.ref('summary_report.summary_report_pdf').with_context(landscape=True).report_action(
            self
        )
