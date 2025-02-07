from odoo import fields, models, api
from odoo.exceptions import UserError


class ResPartnerInherited(models.Model):
    _inherit = "res.partner"

    legal_status = fields.Selection([('individual', 'Individual'), ('partnership', 'Partnership'), ('aop', 'AOP'), ('company', 'Company')], required = True)
    company_reg = fields.Char("Company Registration", required = True)
    artical = fields.Char("Article of Association and Memorandom", required = True)
    strn_no = fields.Char("STRN", required = True)
    cnic_no = fields.Char("CNIC Number", required = True)
    vendor_status = fields.Selection([('active', 'Active'), ('non_active', 'Non Active')], string = "Status")
    major_client = fields.Selection([('a','A Category'), ('b', 'B Category'), ('c', 'C Category')]) 

class ResPartnerBankInherited(models.Model):
    
    _inherit = "res.partner.bank"
    
    bank_iban_num = fields.Char('IBAN Number')



class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)', default=10.00)


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'


    # Override the write method to check purchase tolerance before saving the record
    @api.model
    def write(self, vals):
        # Loop through each record in self (to handle multi-records)
        res =  super(StockPickingInherited, self).write(vals)
        high_perc_qty = 0
        for rec in self:
            if rec.picking_type_id.name == 'Receipts':
                for line in rec.move_ids_without_package:
                    if line.quantity and line.product_uom_qty:
                        
                        high_perc_qty =  line.product_uom_qty + ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100) 
                    if line.quantity >= high_perc_qty:
                        raise UserError('You have violated the purchase tolerance limit')

        # Proceed with the default write behavior after the checks
        return res
