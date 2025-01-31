# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, date_utils, email_split, email_re
from odoo.tools.misc import formatLang, format_date, get_lang
from collections import defaultdict


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_withholding = fields.Monetary(string="Withholding Amount",
        compute='_compute_invoice_withholding_taxes', store=True)
    wht_executed = fields.Boolean(string="WHT Executed")
    count_wht = fields.Boolean(string="Count Withholding ",default = True)                                                                                                            


    @api.depends('line_ids.withholding_tax', 'line_ids.withholding_tax_id')
    def _compute_invoice_withholding_taxes(self):
        for move in self:
            if move.invoice_line_ids:
                move.amount_withholding = sum(rec.withholding_subtotal for rec in move.invoice_line_ids)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    withholding_tax = fields.Boolean(string="Withholding")
    withholding_tax_id = fields.Many2many('account.tax','company_id', string="Withholding Tax", domain=[("withholding_tax", "=", True)])
    withholding_subtotal = fields.Monetary(string="Withholding Subtotal",
        compute='_compute_withholding_subtotal')

    @api.onchange('withholding_tax_id')
    def onchange_withholding_tax_id(self):
        if self.withholding_tax_id:
            if not self.withholding_tax_id.invoice_repartition_line_ids:
                raise ValidationError(_("Warning, please set account in Tax/Withholding Tax (%s, %s)" % (self.product_id.withholding_tax_id.id, self.product_id.withholding_tax_id.name or "")))
            for tax in self.withholding_tax_id.invoice_repartition_line_ids:
                if not tax.account_id and tax.repartition_type == 'tax':
                    raise ValidationError(_("Warning, please set account in Tax/Withholding Tax (%s, %s)" % (self.product_id.withholding_tax_id.id, self.product_id.withholding_tax_id.name or "")))   

    @api.onchange('invoice_line_ids')
    def compute_tax(self):
        for line in self.invoice_line_ids:
            line['withholding_tax_id'] = line.product_id.withholding_tax_id
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id.apply_withholding:
            self.withholding_tax = True
        else:
            self.withholding_tax = False
        
        tax_ids = []
        if self.product_id.apply_withholding and self.product_id.withholding_tax_id:
            if not self.product_id.withholding_tax_id.invoice_repartition_line_ids:
                raise ValidationError(_("Warning, please set account in Tax/Withholding Tax (%s, %s)" % (self.product_id.withholding_tax_id.id, self.product_id.withholding_tax_id.name or "")))
            for tax in self.product_id.withholding_tax_id.invoice_repartition_line_ids:
                if not tax.account_id and tax.repartition_type == 'tax':
                    raise ValidationError(_("Warning, please set account in Tax/Withholding Tax (%s, %s)" % (self.product_id.withholding_tax_id.id, self.product_id.withholding_tax_id.name or "")))
        
            self.update({
               # 'withholding_tax_id': [(6, 0, tax_ids)]
               'withholding_tax_id': self.product_id.withholding_tax_id
            })
        else:
            self.withholding_tax_id = False

    @api.depends('quantity', 'price_unit', 'withholding_tax', 'withholding_tax_id')
    def _compute_withholding_subtotal(self):
        # pass
        for rec in self:
            amount = 0.00
            if rec.withholding_tax and rec.withholding_tax_id:
                for tax in rec.withholding_tax_id:
                    if tax.with_sales_tax == True and tax.basic_tax == True:
                        # amount = (((rec.price_total)) * (tax.amount * 0.01) )
                        amount += ((tax.amount/100) * (rec.price_total) )
                    elif tax.basic_tax == True:
                        # amount = ((rec.quantity * rec.price_unit) * (tax.amount * 0.01) )
                        amount += ((tax.amount/ 100) * (rec.quantity * rec.price_unit))
                    elif tax.with_sales_tax == True:
                        tax_percent = 0
                        if rec.tax_ids:
                            for taxes in rec.tax_ids:
                                tax_percent = taxes.amount
                                # raise UserError(taxes.amount)
                        amount += ((tax.amount/100) * ((tax_percent/100 ) * rec.price_subtotal) )
                        # raise UserError(self.move_id.amount_tax)
                    else:
                        amount = 0.00
                rec.withholding_subtotal = amount
            else:
                rec.withholding_subtotal = 0


class WithholdingLine(models.Model):
    _name = 'withholding.line'

    payment_id = fields.Many2one('account.payment', string="Account Payment")
    account_id = fields.Many2one('account.account', string="Account")
    name = fields.Char(string="Label")
    amount_withholding = fields.Float(string="Amount")
