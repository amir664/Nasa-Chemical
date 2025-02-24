from odoo import api, fields, models ,_
from odoo.exceptions import UserError

class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date",)
    end_date = fields.Date(string="End Date",)
    customer = fields.Many2one('res.partner', string="Customer", default=lambda self: self.env.context.get('default_customer'))
    sales_person = fields.Many2one('res.users', string="Salesperson",related="customer.user_id")
    total_target = fields.Float(string="Total Target")
    total_sales_todate = fields.Float(string="Total Sales Todate")
    line_ids = fields.One2many('customer.target.line','customer_target_id', string="Line Ids", required=True)
    
    
    @api.onchange('line_ids.sales_todate','line_ids.target','line_ids')
    def getTotalSalesAndTargets(self):
        for i in self:
            target = 0
            sales = 0
            for line in i.line_ids:
                target += line.target
                sales += line.sales_todate
            i['total_target'] = target
            i['total_sales_todate'] = sales

    

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target', required=True)
    product_id = fields.Many2one('product.product', required=True)
    target = fields.Float(string="Target", required=True)
    sales_todate = fields.Float(string="Sales Todate", required=True)
    
    # @api.onchange('')
    
class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    target_count = fields.Integer(string="Target Count", required=True)
    def open_customer_targets(self):
        self.get_expense_count()
        return {
            'name': 'Customer Target',
            'domain': [('customer', '=', self.id)],
            'view_type': 'form',
            'res_model': 'customer.target',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context': {'default_customer': self.id}
        }
    
    def get_expense_count(self):
        count = self.env['customer.target'].search_count([('customer', '=', self.id)])
        self.target_count = count

    