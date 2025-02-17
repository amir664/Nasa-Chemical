from odoo import api , fields , models,_
from odoo.exceptions import UserError


class LetterCredit(models.Model):
    _name = "letter.of.credit"
    _description = "Letter Of Credit"
    _rec_name = "name"


    name = fields.Char(string="Name",required=True,copy=False,default=lambda self: _('New'))
    analytic_account_id =fields.Many2one('account.analytic.account',string="Analytic Account")
    currency_id =fields.Many2one('res.currency',string="Currency")
    issuance_of_bank = fields.Char(string="Issuance Of Bank")
    issuance_date = fields.Date(string="Issuance Date")
    expiry_date = fields.Date(string="Expiry Date")
    lc_amount = fields.Float(string="LC Amount")
    lc_type = fields.Selection([('sight','Sight'),('usance','Usance')],string="LC Type")
    state = fields.Selection([('draft','Draft'),('received','Received')],string="State")
    release_count = fields.Integer(string="Processing Count", compute="_compute_release_count")
    release_detail_ids = fields.One2many('lc.processing.release.detail', 'lc_id', string="LC Processing Details")

    def _compute_release_count(self):
        for rec in self:
            rec.release_count = len(rec.release_detail_ids)



    def action_open_release_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'LC Processing Release Details',
            'res_model': 'lc.processing.release.detail',
            'view_mode': 'tree,form',
            'domain': [('lc_id', '=', self.id)],  
            'context': {'default_lc_id': self.id},
        }