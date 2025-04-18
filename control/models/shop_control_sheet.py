from odoo import models, fields

class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    name = fields.Date(string='Shop Control Dated', required=True)
    control_officer = fields.Char(string='Control Officer', required=True)
    toilet_cleaning_ids = fields.One2many('control.toilet_cleaning', 'sheet_id', string='Toilet Cleaning')


class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(default='Tissue Paper In Toilet', readonly=True)
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
