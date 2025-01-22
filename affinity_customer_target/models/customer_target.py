from odoo import api, fields, models ,_
from odoo.exceptions import UserError
 
class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    line_ids = fields.One2many('customer.target.line','customer_target_id', sting="Line Ids")

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target')
    customer = fields.Many2one('res.partner', string="Customer")
    target = fields.Float(string="Target")
