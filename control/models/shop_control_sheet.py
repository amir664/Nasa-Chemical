from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    name = fields.Date(string='Shop Control Dated', required=True)
    control_officer = fields.Char(string='Control Officer', required=True)
    toilet_cleaning_ids = fields.One2many('control.toilet_cleaning', 'sheet_id', string='Toilet Cleaning')



class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet', required=True)
    item = fields.Char(default='Tissue Paper In Toilet', readonly=True)
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')  # <- no required=True
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')  # <- no required=True
    remarks = fields.Text(string='Remarks')  # <- optional

