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
    sales_target = fields.Float(string="Sales Target", required=True)
    # current_sales = fields.Float( string = "Current Sales", readonly=True, required=True, compute= "get_sales_target_sum")

    # @api.depends('customer',"customer_target_id.sale_person_id") 
    # def get_sales_target_sum(self ):
    #     for rec in self:
    #         rec.current_sales = 0
            
    #         records = rec.env['sale.order'].search([('user_id', '=', rec.customer_target_id.sale_person_id.id),('partner_id', '=', rec.customer.id),('state', '!=', 'cancel')])
    #         if records:
                    
    #             total_sales_target = sum(records.mapped('amount_total'))
            
    #             rec.current_sales = total_sales_target
