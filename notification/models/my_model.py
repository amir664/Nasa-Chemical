from odoo import models, fields

class MyModelMain(models.Model):
    _name = 'my.model.main'
    _description = 'Main Form Model'

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='User')
    line_ids = fields.One2many('my.model.line', 'main_id', string='Model Lines')


class MyModelLine(models.Model):
    _name = 'my.model.line'
    _description = 'Lines for Models and Fields'

    main_id = fields.Many2one('my.model.main', string='Main Record')
    # custom_model_id = fields.Many2one('ir.model', string='Model', required=True)
    field_id = fields.Many2one(
    'ir.model.fields',
    string='Field',
    ondelete='set null',
)