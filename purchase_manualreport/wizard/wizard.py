from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'purchase.manualreport'
    _description = 'Purchase Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    product_ids = fields.Many2many('product.template', string='Product')
    vendor_ids = fields.Many2many('res.partner', string = "Vendor")
    po_no = fields.Many2many("purchase.order")
    grn = fields.Many2many("stock.picking")
    invoice_no = fields.Many2many("account.move")
    

    def print_report(self):

        product_ids = []
        if self.product_ids:
            for id in self.product_ids:
                product_ids.append(id.id)

        vendor_ids = []
        if self.vendor_ids:
            for id in self.vendor_ids:
                vendor_ids.append(id.id)
        # grn_ids = self.grn.name if self.grn else []
        grnn=[gr.name    for gr in self.grn] 
        invn=[inv.name    for inv in self.invoice_no] 
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'product_ids': product_ids,
            'vendor_ids': vendor_ids,
            'po_no': self.po_no,
            'grn': grnn,
            'invoice_no': invn
            }

        return self.env.ref('purchase_manualreport.purchase_manualreport_pdf').with_context(landscape=True).report_action(self, data=data)