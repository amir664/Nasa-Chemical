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
    