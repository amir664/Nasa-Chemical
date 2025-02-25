from odoo import api, fields, models ,_
from odoo.exceptions import UserError

class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Sales Target App"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date",)
    end_date = fields.Date(string="End Date",)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                    string="Company",
                                    default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                    related='company_id.currency_id',
                                    default=lambda
                                    self: self.env.user.company_id.currency_id.id)
    customer = fields.Many2one('res.partner', string="Customer", default=lambda self: self.env.context.get('default_customer'))
    sales_person = fields.Many2one('res.users', string="Salesperson",related="customer.user_id")
    
    total_target = fields.Monetary(string="Target")
    sales_todate = fields.Monetary(string="Sales Achieved",readonly=True,compute="getTotalSales")
    line_ids = fields.One2many('customer.target.line','customer_target_id', string="Line Ids", required=True)
    
    
    @api.depends('customer.sale_order_count')
    def getTotalSales(self):
        for i in self:
            amount = 0
            sale_orders = i.env['sale.order'].search([('partner_id.id','=',i.customer.id),('state','not in',['draft','cancel'])])
            for so in sale_orders:
                amount += so.amount_total
            i['sales_todate'] = amount


class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target', required=True)
    product_id = fields.Many2one('product.product', required=True)
    target = fields.Float(string="Target (CTN)", required=True)
    sales_todate = fields.Float(string="Sales Achieved", required=True,compute="getTotalSales")
    
    @api.depends('customer_target_id.customer.sale_order_count')
    def getTotalSales(self):
        for i in self:
            qty = 0
            sale_order_line = i.env['sale.order.line'].search([('order_id.partner_id.id','=',i.customer.id),('order_id.state','not in',['draft','cancel']),('product_id.id','=',i.product_id.id)])
            for sol in sale_order_line:
                qty += sol.product_uom_qty
            i['sales_todate'] = qty
    
    
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

    