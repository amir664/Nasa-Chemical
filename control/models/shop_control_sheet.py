from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    name = fields.Date(string='Shop Control Dated', required=True)
    control_officer = fields.Char(string='Control Officer', required=True)
    toilet_cleaning_ids = fields.One2many('control.toilet_cleaning', 'sheet_id', string='Toilet Cleaning')

    @api.model
    def default_get(self, fields_list):
        """ Override default_get to prepopulate the toilet cleaning items """
        res = super(ShopControlSheet, self).default_get(fields_list)
        
        # Predefined items to add
        default_items = [
            'Tissue Paper In Toilet',
            'Spray In Toilet',
            'Hand Soap Lotion',
            'Cleanness of Flush',
            'Cleanness of Floor',
            'Dusbin',
        ]
        
        # Create default toilet cleaning entries and set them in the res dict
        toilet_cleaning_data = []
        for item in default_items:
            toilet_cleaning_data.append((0, 0, {'item': item}))
        
        # Set the default values for the One2many field (toilet_cleaning_ids)
        res.update({
            'toilet_cleaning_ids': toilet_cleaning_data,
        })
        return res


class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)
