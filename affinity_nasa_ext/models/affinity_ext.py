from odoo import fields, models, api
from odoo.exceptions import UserError

# class ProductCategoryInherited(models.Model):
#     _inherit = 'product.category'

#     company_id = fields.Many2one('res.company', string = 'Companies', default=lambda self: self.env.company)

class PurchaseRerquestLineInherited(models.Model):
    _inherit = 'purchase.request.line'

    minimum_stock_level = fields.Float('Minimum Stock Level')
    forecasting_stock = fields.Float('Forecasting Stock')
    date_due = fields.Datetime('Date Due', required = True)
  

    # @api.depends('product_id')
    # def _compute_stock_level(self):
        
    #     for rec in self:
    #         order = self.env['stock.warehouse.orderpoint'].search([('product_id', '=', rec.product_id.id)])    
    #         if order:    
    #             rec['minimum_stock_level'] = order.product_min_qty

class QualityPoints(models.Model):
    _inherit = 'quality.point'
    
    methods = fields.Char(string="Methods")
    quality_parameters = fields.Selection([('physical','Physical Property'),('chemical','Chemical Property')])



class ProductTemplate(models.Model):
    _inherit = 'product.tempalte'
    
    hs_code = fields.Char(string="HS Code")
    




