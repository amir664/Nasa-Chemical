from odoo import _, api, fields, models


class POReportWizard(models.TransientModel):
    _name = 'po.analysis'
    _description = 'Purchase Order Analysis Report'
    
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    product_ids = fields.Many2many('product.template', string='Product')
    warehouse_id = fields.Many2one('stock.warehouse', string = "Ware House")
    vendor_ids = fields.Many2many('res.partner', string='Vendor')
    # po_no = fields.Char(string = "po_no")
    # grn = fields.Char(string = "grn")
    po_no = fields.Many2many("purchase.order", string="PO Number")
    grn = fields.Many2many("stock.picking", string="GRN")

    
    

    def print_report(self):

        product_ids = []
        if self.product_ids:
            for id in self.product_ids:
                product_ids.append(id.id)
        
        vendor_ids = []
        if self.vendor_ids:
            for id in self.vendor_ids:
                vendor_ids.append(id.id)

        po_ids = self.po_no.ids if self.po_no else []
        grn_ids = self.grn.ids if self.grn else []

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'product_ids': product_ids,
            'warehouse_id': self.warehouse_id.id,
            'vendor_ids': vendor_ids,
            'po_ids': po_ids,  # Change key to `po_ids`
            'grn_ids': grn_ids  # Change key to `grn_ids`
        }
    
            # data = {
            #     'date_from': self.date_from,
            #     'date_to': self.date_to,
            #     'product_ids': product_ids,
            #     'warehouse_id': self.warehouse_id.id,
            #     'vendor_ids': vendor_ids,
            #     'po_no': self.po_no,
            #     'grn': self.grn
            #     }

        return self.env.ref('po_analysis.po_analysis_pdf').with_context(landscape=True).report_action(self, data=data)