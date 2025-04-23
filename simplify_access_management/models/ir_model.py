# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools,_

class ir_model(models.Model):
    _inherit = 'ir.model'

    abstract = fields.Boolean('Abstract', readonly=True)



class ir_module_module(models.Model):
    _inherit = 'ir.module.module'


    def _button_immediate_function(self, function):
        res = super(ir_module_module, self)._button_immediate_function(function)
        if function.__name__ in ['button_install', 'button_upgrade']:
            for record in self.env['ir.model'].search([]):
                if record.name == 'Email Thread':
                    print()
                record.abstract = self.env[record.model]._abstract
        return res