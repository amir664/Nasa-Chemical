from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    sequence_number = fields.Char(string='Number', copy=False, readonly=True)

    @api.model
    def create(self, vals):
        if self.env.context.get('default_customer_rank', 0) > 0:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('res.partner.customer.sequence')
        elif self.env.context.get('default_supplier_rank', 0) > 0:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('res.partner.vendor.sequence')
        return super(InheritResPartner, self).create(vals)
