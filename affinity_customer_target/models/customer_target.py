from odoo import api, fields, models ,_
from odoo.exceptions import UserError
 
class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    line_ids = fields.One2many('customer.target.line','customer_target_id', sting="Line Ids", required=True)
    sale_person_id = fields.Many2one('res.users',string="Sale Person ID", required=True)
    sale_person_name = fields.Char(string="Sale Person Name", required=True)
    region = fields.Char(string="Region", required=True)

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target', required=True)
    customer = fields.Many2one('res.partner', string="Customer", required=True)
    sales_target = fields.Float(string="Sales Target", required=True)
    current_sales = fields.Float( string = "Current Sales", readonly=True, required=True)

    @api.depends('customer',"customer_target_id.sale_person_id")
    def get_sales_target_sum(self ):
        records = self.env['sale.order'].search([('user_id', '=', self.customer_target_id.sale_person_id.id),('partner_id', '=', self.customer.id),('state', '!=', 'cancel')])
        total_sales_target = sum(records.mapped('amount_total'))
        
        self.current_sales = total_sales_target
