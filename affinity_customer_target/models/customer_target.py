from odoo import api, fields, models ,_
from odoo.exceptions import UserError
 
class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    line_ids = fields.One2many('customer.target.line','customer_target_id', sting="Line Ids")
    sale_person_id = fields.Many2one('res.users',string="Sale Person ID")
    sale_person_name = fields.Char(string="Sale Person Name")
    region = fields.Char(string="Region")

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target')
    customer = fields.Many2one('res.partner', string="Customer")
    sales_target = fields.Float(string="Sales Target")
    current_sales = fields.Float( string = "Current Sales")

    @api.onchange('customer')
    def get_sales_target_sum(self ):
        records = self.env['sale.order'].search([('user_id', '=', self.sale_person_id.id),('partner_id', '=', self.customer.id),('state', '!=', 'cancel')])
        total_sales_target = sum(records.mapped('amount_total'))
        
        self.current_sales = total_sales_target
