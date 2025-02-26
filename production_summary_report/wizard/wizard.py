from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MrpProductionReportWizard(models.TransientModel):
    _name = 'mrp.production.report'
    _description = 'MRP Production Report Wizard'

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    product_id = fields.Many2one('product.product', string="Product")

    def action_generate_report(self):
        """Redirects to the report page with filters."""
        if self.date_from > self.date_to:
            raise ValidationError("Date From cannot be greater than Date To.")
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/mrp_production_report?date_from=%s&date_to=%s&product_id=%s' % (
                self.date_from, self.date_to, self.product_id.id if self.product_id else ''
            ),
            'target': 'new',
        }
