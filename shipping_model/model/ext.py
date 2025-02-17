from odoo import api , fields , models,_
from odoo.exceptions import UserError


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    shipping_count = fields.Integer(string="Shipping Count", compute="compute_shipping_count")
    shipping_detail_ids = fields.One2many('shipment.model', 'analytic_account_id', string="Shipping Details")
    letter_credit_count = fields.Integer(string="Shipping Count", compute="compute_letter_credit_count")
    letter_credit_detail_ids = fields.One2many('letter.of.credit', 'analytic_account_id', string="Letter Of Credit Details")
    analytic_account_id =fields.Many2one('account.analytic.account',string="Analytic Account")
    
    def compute_shipping_count(self):
        for rec in self:
            rec.shipping_count = len(rec.shipping_detail_ids)


    def action_open_shipping(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Shipping',
            'res_model': 'shipment.model',
            'view_mode': 'tree,form',
            'domain': [('analytic_account_id', '=', self.id)],  
            'context': {'default_analytic_account_id': self.id,'default_shipping_name':self.name},
        }

    def compute_letter_credit_count(self):
        for rec in self:
            rec.letter_credit_count = len(rec.letter_credit_detail_ids)


    def action_open_letter_credit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Letter Of Credit',
            'res_model': 'letter.of.credit',
            'view_mode': 'tree,form',
            'domain': [('analytic_account_id', '=', self.id)],  
            'context': {'default_analytic_account_id': self.id,'default_name':self.name},
        }


