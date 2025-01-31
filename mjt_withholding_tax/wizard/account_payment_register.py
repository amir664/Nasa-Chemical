# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    wht_tax_line_ids = fields.One2many("withholding.tax.line", 'payment_reg_id', string="Payment Register Line")
    count_wht = fields.Boolean(string="Count Withholding " , default = True)                                                                                                            


    # @api.model                                                                                                    
    tax_ids = []
    data_list = []
    def _get_wizard_values_from_batch(self, batch_result):
        print("_get_wizard_values_from_batch OVERRIDE RUNNING..................")
        res = super(AccountPaymentRegister, self)._get_wizard_values_from_batch(batch_result)
        temp = []
        if batch_result:
            move_id = False
            for data in batch_result['lines'][:1]:
                move_line_id = self.env['account.move.line'].browse(data.id)
                move_id = move_line_id.move_id
            if move_id:
                wht_tax_ids = []
                for rec in move_id.invoice_line_ids:
                    for wht_id in rec.withholding_tax_id:
                        if wht_id and wht_id.id not in wht_tax_ids:
                            wht_tax_ids.append(wht_id.id)
                for tax in wht_tax_ids:
                    subtotal_amount = 0
                    for move in move_id.invoice_line_ids:
                        for wht_id in move.withholding_tax_id:
                            if wht_id and wht_id.id == tax:
                                if wht_id.basic_tax ==  True and wht_id.with_sales_tax == True:
                                    subtotal_amount += (wht_id.amount/100) * move.price_total
                                elif wht_id.basic_tax ==  True:
                                    subtotal_amount += (wht_id.amount/100) * move.price_subtotal
                                elif wht_id.with_sales_tax ==  True:
                                    for taxes in move.tax_ids:
                                        subtotal_amount += ((wht_id.amount/100) * ((taxes.amount/100) * move.price_subtotal))
                    tax_id = self.env['account.tax'].browse(tax)
                    vals = {
                        "tax_id": tax,
                        "name": tax_id.name,
                        "amount_withholding": subtotal_amount,
                    }
                    temp.append((0, 0, vals))  
                self.write({"wht_tax_line_ids": False})
                self.write({"wht_tax_line_ids": temp})
            if move_id.wht_executed == True:
                wht_tax_ids = []
                for rec in move_id.invoice_line_ids:
                    for wht_id in rec.withholding_tax_id:
                        if wht_id and wht_id.id not in wht_tax_ids:
                            wht_tax_ids.append(wht_id.id)
                for tax in wht_tax_ids:
                    subtotal_amount = 0
                    remain_subtotal_amount = 0
                    vals = {}
                    temp = []
                    jv = self.env['account.move'].search([('ref','=',move_id.name)])
                    # raise UserError(jv[0])
                    if jv:
                        for ml in move_id.invoice_line_ids:
                            for j in jv[0]: 
                                for wht_id in ml.withholding_tax_id:
                                    for jl in j.line_ids:
                                        if jl.name == wht_id.name:
                                            if wht_id.basic_tax ==  True and wht_id.with_sales_tax == True:
                                                subtotal_amount += (wht_id.amount/100) * ml.price_total
                                            elif wht_id.basic_tax ==  True:
                                                subtotal_amount += (wht_id.amount/100) * ml.price_subtotal
                                            elif wht_id.with_sales_tax ==  True:
                                                for taxes in ml.tax_ids:    
                                                    subtotal_amount += ((wht_id.amount/100) * ((taxes.amount/100) * ml.price_subtotal))
                                            for tj in jv:
                                                for tjl in tj.line_ids:
                                                    if tjl.name == wht_id.name:
                                                        subtotal_amount -= tjl.credit 
                                            # raise UserError(subtotal_amount)
                                            if not subtotal_amount  <= 1:             
                                                tax_id = self.env['account.tax'].browse(tax)
                                                vals = {
                                                    "tax_id": wht_id.id,
                                                    "name": wht_id.name,
                                                    "amount_withholding": subtotal_amount,
                                                }
                                                temp.append((0, 0, vals))  
                                                # raise UserError(subtotal_amount)
                                                subtotal_amount = 0 
                                                self.write({"wht_tax_line_ids": False})
                                                self.write({"wht_tax_line_ids": temp})
                                                                        
        return res




    @api.depends('source_amount', 'source_amount_currency', 'source_currency_id', 'company_id', 'currency_id', 'payment_date')
    def _compute_amount(self):
        print("----_compute_amount OVERRIDE RUNNING")
        for wizard in self:
            wht_amount = 0
            if wizard.wht_tax_line_ids:
                wht_amount = sum(rec.amount_withholding for rec in wizard.wht_tax_line_ids)
            
            if wizard.source_currency_id == wizard.currency_id:
                # Same currency.
                wizard.amount = wizard.source_amount_currency - wht_amount
            elif wizard.currency_id == wizard.company_id.currency_id:
                # Payment expressed on the company's currency.
                wizard.amount = wizard.source_amount - wht_amount
            else:
                # Foreign currency on payment different than the one set on the journal entries.
                amount_payment_currency = wizard.company_id.currency_id._convert(wizard.source_amount, wizard.currency_id, wizard.company_id, wizard.payment_date)
                wizard.amount = amount_payment_currency - wht_amount


    @api.depends('amount')
    def _compute_payment_difference(self):
        print("_compute_payment_difference OVERRIDE RUNNING..")
        for wizard in self:
            wht_amount = 0
            if wizard.wht_tax_line_ids:
                wht_amount = sum(rec.amount_withholding for rec in wizard.wht_tax_line_ids)
            if wizard.source_currency_id == wizard.currency_id:
                # Same currency.
                wizard.payment_difference = wizard.source_amount_currency - wizard.amount - wht_amount
            elif wizard.currency_id == wizard.company_id.currency_id:
                # Payment expressed on the company's currency.
                wizard.payment_difference = wizard.source_amount - wizard.amount - wht_amount
            else:
                # Foreign currency on payment different than the one set on the journal entries.
                amount_payment_currency = wizard.company_id.currency_id._convert(wizard.source_amount, wizard.currency_id, wizard.company_id, wizard.payment_date)
                wizard.payment_difference = amount_payment_currency - wizard.amount - wht_amount

            # raise UserError("s")

    def _create_payments(self):
        res = super(AccountPaymentRegister, self)._create_payments()
        print("_create_payments OVERRIDE RUNNING........................")
        # raise UserError('working')
        wht_wizard = []
        if self.wht_tax_line_ids:
            for rec in self.wht_tax_line_ids:
                account_ids = rec.tax_id.invoice_repartition_line_ids.mapped('account_id')
                if account_ids:
                    account_id = account_ids[0]
                    # if self.count_wht == True:
                    wizard_vals = {
                        'account_id': account_id.id,
                        'amount_wht': rec.amount_withholding,
                        'name': rec.name
                    }
                    wht_wizard.append((0, 0, wizard_vals))
            # raise UserError(str(wht_wizard))
            payment_id = self.env['account.payment'].browse(res.id)
            res.move_id.button_draft()
            # print("---WHTWIZARD", wht_wizard)

            res.write({
                'is_wht_trx': True,
                'wht_line_ids': wht_wizard
                })
            res.move_id._check_balanced(self)
            res.action_post() 

            batches = self._get_batches()
            edit_mode = self.can_edit_wizard and (len(batches[0]['lines']) == 1 or self.group_payment)
            to_reconcile = []
            if edit_mode:
                payment_vals = self._create_payment_vals_from_wizard(self)
                payment_vals_list = [payment_vals]
                to_reconcile.append(batches[0]['lines'])
                # raise UsesrError(str(to_reconcile))
                # raise UserError(str(batches))
            else:
                # Don't group payments: Create one batch per move.
                if not self.group_payment:
                    new_batches = []
                    # raise User
                    for batch_result in batches:
                        for line in batch_result['lines']:
                            new_batches.append({
                                **batch_result,
                                'lines': line,
                            })
                    batches = new_batches
                # raise UserError(batches)

                payment_vals_list = []
                for batch_result in batches:
                    payment_vals_list.append(self._create_payment_vals_from_batch(batch_result))
                    to_reconcile.append(batch_result['lines'])

            domain = [('account_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False)]
            for payment, lines in zip(res, to_reconcile):
                # When using the payment tokens, the payment could not be posted at this point (e.g. the transaction failed)
                # and then, we can't perform the reconciliation.
                # raise UserError('0002 /// /// ' + str(lines.withholding_subtotal))
                if payment.state != 'posted':
                    continue

                payment_lines = payment.line_ids.filtered_domain(domain)
                for account in payment_lines.account_id:
                    (payment_lines + lines).filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)]).reconcile()
            invoice_id = self.env['account.move'].search([('name','=',res.ref)], limit=1)
            # if invoice_id:
            #     invoice_id.write({
            #         'wht_executed': True
            #         })
                
        return res


class WithholdingTaxLine(models.TransientModel):
    _name = 'withholding.tax.line'

    payment_reg_id = fields.Many2one('account.payment.register', string="Account Payment Register")
    tax_id = fields.Many2one('account.tax', string="Taxes")
    name = fields.Char(string="Description")
    amount_withholding = fields.Float(string="Amount WHT")
    count_wth = fields.Boolean(String = "Count WTH",default = False)


# dicts = {}
# values = ["Hi", "I"]
# keys = ["12", "13"]
# for i in keys:
#     for x in values:
#         dicts[i] = x
# print(dicts)