from odoo import api, fields, models ,_
from odoo.exceptions import UserError

class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date",)
    end_date = fields.Date(string="End Date",)
    customer = fields.Many2one('res.partner', string="Customer",)
    line_ids = fields.One2many('customer.target.line','customer_target_id', sting="Line Ids", required=True)
    

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target', required=True)
    product_id = fields.Many2one('product.product', required=True)
    target = fields.Float(string="Target", required=True)
    
class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    target_count = fields.Integer(string="Target Count", required=True)
    def open_customer_targets(self):
        return {
            'name': 'Customer Target',
            'domain': [('customer', '=', self.id)],
            'view_type': 'form',
            'res_model': 'res.partner',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
    
    def get_expense_count(self):
        count = self.env['res.partner'].search_count([('customer', '=', self.id)])
        self.target_count = count

    