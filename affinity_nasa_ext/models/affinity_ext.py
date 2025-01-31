from odoo import fields, models, api
from odoo.exceptions import UserError
from num2words import num2words

# class ProductCategoryInherited(models.Model):
#     _inherit = 'product.category'

#     company_id = fields.Many2one('res.company', string = 'Companies', default=lambda self: self.env.company)

class PurchaseRerquestLineInherited(models.Model):
    _inherit = 'purchase.request.line'

    minimum_stock_level = fields.Float('Minimum Stock Level')
    forecasting_stock = fields.Float('Forecasting Stock')
    on_hand_qty = fields.Float('On Hand Quantity')
    
    
    @api.onchange('product_id')
    def _on_change_product_id(self):
        for rec in self:
            
            order = rec.env['stock.warehouse.orderpoint'].search([('product_id', '=', rec.product_id.id)])
            # Search for the stock quant for the product
            quant = rec.env['stock.quant'].search([('product_id', '=', rec.product_id.id), ('location_id.usage', '=', 'internal')])
            
            # If a warehouse orderpoint is found
            if rec.product_id:
                if rec.product_id == order.product_id:
                    # Set minimum stock level and forecasting stock from orderpoint
                    rec['minimum_stock_level'] = order.product_min_qty
                    rec['forecasting_stock'] = order.qty_forecast

            # If a stock quant is found in an internal location
            if quant:
                for quan in quant:
                    if rec.product_id == quan.product_id:
                        # Set on hand quantity from quant
                        rec['on_hand_qty'] = quan.inventory_quantity_auto_apply



class PurchaseOrderLineInherited(models.Model):
    _inherit = 'purchase.order.line'

    payment_terms = fields.Many2one('account.payment.term', string = "Payment Terms",compute="compute_pt")

    @api.depends('order_id.payment_term_id')
    def compute_pt(self):
        for line in self:
            if line.order_id and line.order_id.payment_term_id:
                line.payment_terms = line.order_id.payment_term_id
            else:
                line.payment_terms = False
    # @api.model
    # def write(self, vals):
    #     # Loop through each record in self (to handle multi-records)
    #     res =  super(PurchaseOrderLineInherited, self).write(vals)
    #     for rec in self:
    #         order = rec.env['purchase.order'].search([('order_id', '=', rec.id)])
    #         if order:
    #             # raise UserError("pawan")
            
    #             if rec.payment_term_id:
    #                 rec['payment_terms'] = order.payment_term_id

    #     # Proceed with the default write behavior after the checks
    #     return res


class PurchaseRerquestInherited(models.Model):
    _inherit = 'purchase.request'

    department = fields.Char('Department', compute = "get_department")
    date_due = fields.Datetime('Due Date', required = True)
  

    @api.depends('requested_by')
    def get_department(self):
        
        for rec in self:
            rec['department'] = ""
            if rec.requested_by:
                rec['department'] = rec.requested_by.department_id.name

    
    # @api.model
    # def write(self, vals):
    #     # Loop through each record in self (to handle multi-records)
    #     res =  super(PurchaseRerquestInherited, self).write(vals)
    #     for rec in self:
    #         for line in rec.line_ids:
    #             # Search for the stock warehouse orderpoint for the product
    #             order = rec.env['stock.warehouse.orderpoint'].search([('product_id', '=', line.product_id.id)])
    #             # Search for the stock quant for the product
    #             quant = rec.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal')])
                
    #             # If a warehouse orderpoint is found
    #             if order:
    #                 if line.product_id == order.product_id:
    #                     # Set minimum stock level and forecasting stock from orderpoint
    #                     line['minimum_stock_level'] = order.product_min_qty
    #                     line['forecasting_stock'] = order.qty_forecast

    #             # If a stock quant is found in an internal location
    #             if quant:
    #                 if line.product_id == quant.product_id:
    #                     # Set on hand quantity from quant
    #                     line['on_hand_qty'] = quant.inventory_quantity_auto_apply


    #     # Proceed with the default write behavior after the checks
    #     return res

                


class QualityPoints(models.Model):
    _inherit = 'quality.point'
    
    methods = fields.Char(string="Methods")
    quality_parameters = fields.Selection([('physical','Physical Property'),('chemical','Chemical Property')])


# class QualityCheckInherited(models.Model):
    
#     _inherit = "quality.check"
    
#     def do_progress(self):
#         # for rec in self:
#             # if rec.quality_state:
#         self.quality_state = 'in_progress'



class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)', default=10.00)
    new_code = fields.Char(string="New Code")

    def write(self, vals):
        for rec in self:
            current_category = rec.categ_id
            if not rec.new_code:
                while current_category.parent_id:
                    current_category = current_category.parent_id

                if current_category.id == 1050:
                    vals['new_code'] = self.env['ir.sequence'].next_by_code('raw')
                elif current_category.id == 1113:
                    vals['new_code'] = self.env['ir.sequence'].next_by_code('packing')
                elif current_category.id == 1003:
                    vals['new_code'] = self.env['ir.sequence'].next_by_code('finished')
                elif current_category.id == 1543:
                    vals['new_code'] = self.env['ir.sequence'].next_by_code('semi')

        return super(ProductTemplateInherited, self).write(vals)

           





class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    amount_in_words = fields.Char(string='Amount in Words', compute='_compute_amount_in_words')
    
    @api.depends('amount_total')
    def _compute_amount_in_words(self):
        for payment in self:
            if payment.amount_total:
                payment.amount_in_words = num2words(payment.amount_total, lang='en').title()
            else:
                payment.amount_in_words = ''

class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    # @api.constrains('state')
    # def not_validate(self):
    #     for rec in self:
    #         qccheck = self.env['quality.check'].search([('picking_id','=',rec.id)])
    #         if qccheck:
    #             for qc in qccheck:
    #                 if qc.state == "done":
    #                     raise UserError("State cannot move forward to done stage when qc is failed")

    # Override the write method to check purchase tolerance before saving the record
    @api.model
    def write(self, vals):
        # Loop through each record in self (to handle multi-records)
        res =  super(StockPickingInherited, self).write(vals)
        high_perc_qty = 0
        # low_perc_qty = 0
        for rec in self:
            if rec.picking_type_id.name == 'Receipts':
                for line in rec.move_ids_without_package:
                    if line.quantity and line.product_uom_qty:
                        
                        high_perc_qty =  line.product_uom_qty + ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100) 
                        # low_perc_qty =  line.product_uom_qty - ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100 )
                        
                        # raise UserError(str(high_perc_qty))
                        # or line.quantity < low_perc_qty:
                        
                    if line.quantity > high_perc_qty:
                        raise UserError('You have violated the purchase tolerance limit')

        # Proceed with the default write behavior after the checks
        return res


class SaleOrderLineInherited(models.Model):
    _inherit = 'sale.order.line'

    is_discount = fields.Selection(selection=[('yes', 'Yes'),('no', 'No')],string='Is Discount',default='no')

class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    amount_in_words = fields.Char(string='Amount in Words', compute='_compute_amount_in_words')
    comments = fields.Text('Comments')

    cust_ref_no = fields.Char('Customer Reference Number')
    
    @api.depends('amount_total')
    def _compute_amount_in_words(self):
        for payment in self:
            if payment.amount_total:
                payment.amount_in_words = num2words(payment.amount_total, lang='en').title()
            else:
                payment.amount_in_words = ''


        

