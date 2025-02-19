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

        # Processing data according to filters
        report_data = []
        for po in purchase_orders:
            for line in po.order_line:
                # If specific items are selected, filter only those
                if self.item_wise and line.product_id not in self.item_wise:
                    continue

                entry = {
                    'vendor': po.partner_id.name,
                    'po': po.name,
                    'item': line.product_id.name,
                    'quantity': line.product_qty,
                    'uom': line.product_uom.name,
                    'amount': line.price_total
                }

                # Determine grouping
                if self.item_wise:
                    entry['grouping'] = "Item Wise"
                elif hasattr(self, 'vendor_accounts_wise') and self.vendor_accounts_wise:
                    entry['grouping'] = "Vendor Accounts Wise"
                elif hasattr(self, 'vendor_group_wise') and self.vendor_group_wise:
                    entry['grouping'] = "Vendor Group Wise"
                elif hasattr(self, 'item_group_wise') and self.item_group_wise:
                    entry['grouping'] = "Group of Item Wise"
                else:
                    entry['grouping'] = "General"

                report_data.append(entry)

        # Return report action with formatted data
        return self.env.ref('summary_report.summary_report_pdf').with_context(landscape=True).report_action(
            self, data={'report_data': report_data}
        )
