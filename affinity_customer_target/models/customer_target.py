from odoo import api, fields, models ,_
from odoo.exceptions import UserError
 
class CustomerTarget(models.Model):
    _name="customer.target"
    _description="Customer Target App"

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    line_ids = fields.One2many('customer.target.line','customer_target_id', sting="Line Ids")
    sale_person_id = fields.Char(string="Sale Person ID")
    sale_person_name = fields.Char(string="Sale Person Name")
    origin = fields.Char(string="Origin")

class CustomerTargetLine(models.Model):
    _name="customer.target.line"
    _description = "Customer Target Line"

    customer_target_id = fields.Many2one('customer.target')
    customer = fields.Many2one('res.partner', string="Customer")
    sales_target = fields.Float(string="Sales Target")
    current_sales = fields.Float( string = "Current Sales",  compute='_compute_current_sales', store=True)

    @api.depends('sales_target')
    def _compute_current_sales(self):
        for record in self:
            total = sum(self.search([]).mapped('sales_target'))
            record.current_sales = total
