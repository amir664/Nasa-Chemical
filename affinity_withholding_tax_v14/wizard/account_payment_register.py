import logging
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


_logger = logging.getLogger(__name__)

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    wht_lines = fields.One2many('withholding.lines','wizard_id',string="Withholding Lines")
    wht_account = fields.Many2one('account.account',string="Witholding Account")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        communication = defaults.get('communication')
        if communication:
            account_move = self.env['account.move'].search([('name', '=', communication)], limit=1)
            if account_move.move_type == 'out_invoice':
                defaults['wht_account'] = 8     # Customer invoice
            elif account_move.move_type == 'in_invoice':
                defaults['wht_account'] = 1157  # Vendor bill

        return defaults


    def _create_payments(self):
        res = super(AccountPaymentRegister, self)._create_payments()
        _logger.info("_create_payments OVERRIDE RUNNING........................")

        # debit_line = next(filter(lambda line: line.credit == 0, res.move_id.line_ids), None)
        # credit_line = next(filter(lambda line: line.debit == 0, res.move_id.line_ids), None)
        # lines = []
        # for i in self.wht_lines:
        #     if res.payment_type == 'outbound':
        #         lines.append((0, 0, {
        #                 'account_id': i.wht_account.id,
        #                 'debit': 0,
        #                 'credit': i.wht_amount,
        #                 'partner_id': res.move_id.partner_id,
        #                 'name': i.name,
        #             }))

        #         credit_line.with_context(check_move_validity=False).credit = res.amount -  i.wht_amount
        #     if res.payment_type == 'inbound':
        #         lines.append((0, 0, {
        #                 'account_id': i.wht_account.id,
        #                 'debit': i.wht_amount,
        #                 'credit': 0,
        #                 'partner_id': res.move_id.partner_id,
        #                 'name': i.name,
        #             }))

        #         debit_line.with_context(check_move_validity=False).debit -= i.wht_amount
        # res.with_context(check_move_validity=False).write({
        #         'line_ids': lines,
        #     })
        return res


       

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'write_off_line_vals': [],
            # WHT
            'wht_lines':self.wht_lines,
            # custom fields
            # 'x_studio_cheque_no':self.x_studio_cheque_no,
            # 'ref': self.communication
        }
        return payment_vals

class Withholdinglines(models.TransientModel):
    _name = "withholding.lines"

    name = fields.Char(string="Lable")
    wizard_id = fields.Many2one('account.payment.register',string="Wizard Id")
    payment_id = fields.Many2one('account.payment',string="Payment Id")
    # amount_to_withhold = fields.Float(string="Amount To Withhold")
    wht_amount = fields.Float(string="Witholding Amount")
    wht_code = fields.Many2one('account.tax',string="Tax Code")
    wht_account = fields.Many2one('account.account',string="Witholding Account")

   


    @api.onchange('wht_code')
    def getTaxAmount(self):
        for i in self:
            if i.wht_code:
                # if i.amount_to_withhold <= 0 or i.wht_code.amount <= 0:
                #     raise ValidationError("Total amount and percentage must be non-negative.")
                i['wht_amount'] =  (i.wizard_id.amount * i.wht_code.amount) / 100
                for line in i.wht_code.invoice_repartition_line_ids:
                    if line.account_id:
                        i['wht_account'] =  line.account_id.id