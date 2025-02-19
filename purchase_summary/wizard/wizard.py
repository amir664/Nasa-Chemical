from odoo import models, fields, api

class PSReportWizard(models.TransientModel):
    _name = 'summary.report'
    _description = 'Purchase Order Summary Report'
    
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)])
    item_wise = fields.Many2many('product.product', string="Item(s)")

    
    def print_report(self):
        """
        Generates the purchase order summary report based on the selected filters.
        """

        domain = []
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))
        if self.vendor_id:
            domain.append(('partner_id', '=', self.vendor_id.id))
        if self.item_wise:
            domain.append(('order_line.product_id', 'in', self.item_wise.ids))

        # Fetch purchase order data based on filters
        purchase_orders = self.env['purchase.order'].search(domain)

        # Collect unique item names
        item_names = set()
        for po in purchase_orders:
            for line in po.order_line:
                if not self.item_wise or line.product_id in self.item_wise:
                    item_names.add(line.product_id.name)

        # Return report action with item names only
        return self.env.ref('summary_report.summary_report_pdf').with_context(landscape=True).report_action(
            self, data={'items': list(item_names)}
        )
