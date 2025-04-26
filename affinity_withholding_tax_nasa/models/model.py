from odoo import api, fields, models,_
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = "account.payment"

    wht_lines = fields.One2many('withholding.lines','payment_id',string="Withholding Lines")

    def action_post(self):
        debit_line = next(filter(lambda line: line.credit == 0, self.move_id.line_ids), None)
        credit_line = next(filter(lambda line: line.debit == 0, self.move_id.line_ids), None)
        lines = []
        amount = 0
        # raise UserError(self.move_id.line_ids)
        for ids in self.move_id.line_ids:
            if ids.id != debit_line.id and ids.id != credit_line.id:
                if self.payment_type == 'outbound':
                    amount += ids.credit
                    credit_line.with_context(check_move_validity=False).credit += amount
                    ids.with_context(check_move_validity=False).unlink()

                if self.payment_type == 'inbound':
                    amount += ids.debit
                    debit_line.with_context(check_move_validity=False).debit += amount
                    ids.with_context(check_move_validity=False).unlink()

        
        for i in self.wht_lines:
            if self.payment_type == 'outbound':
                lines.append((0, 0, {
                        'account_id': i.wht_account.id,
                        'debit': 0,
                        'credit': i.wht_amount,
                        'partner_id': self.move_id.partner_id,
                        'name': i.name,
                    }))

                credit_line.with_context(check_move_validity=False).credit = self.amount -  i.wht_amount
            if self.payment_type == 'inbound':
                lines.append((0, 0, {
                        'account_id': i.wht_account.id,
                        'debit': i.wht_amount,
                        'credit': 0,
                        'partner_id': self.move_id.partner_id,
                        'name': i.name,
                    }))

                debit_line.with_context(check_move_validity=False).debit -= i.wht_amount
        self.with_context(check_move_validity=False).write({
                'line_ids': lines,
            })
        res = super(AccountPayment,self).action_post()
        return res