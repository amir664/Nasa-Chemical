from odoo import models, fields

class MrpProductionReportWizard(models.TransientModel):
    _name = 'mrp.production.report.wizard'
    _description = 'MRP Production Report Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    product_id = fields.Many2many('product.product', string="Product")
    category_id = fields.Many2one('product.category', string="Product Category")
    item_type = fields.Selection([
        ('fg', 'Finished Goods (FG)'),
        ('sfg', 'Semi-Finished Goods (SFG)'),
        ('both', 'Both')
    ], string="Item Type", default='both')

    def generate_report(self):
        """Redirects to the report controller with filters as URL params."""
        return {
            'type': 'ir.actions.act_url',
            'url': f"/mrp_production_report?date_from={self.date_from}&date_to={self.date_to}"
                   f"&product_id={self.product_id.id if self.product_id else ''}"
                   f"&category_id={self.category_id.id if self.category_id else ''}"
                   f"&item_type={self.item_type}",
            'target': 'self',
        }
