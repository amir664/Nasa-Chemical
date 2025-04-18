from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ShopControlSheet(models.Model):
    _name = 'control.warehouse_control_sheet'
    _description = 'Warehouse Control Sheet'

    name = fields.Date(string='Shop Control Dated')
    control_officer3 = fields.Many2one('res.users',string='Control Officer Dated')
    packing_room_ids = fields.One2many('control.packing_room', 'sheet_id', string='Packing Room')
    toilet_cleaning_women_ids = fields.One2many('control.toilet_cleaning_women', 'sheet_id')
    toilet_cleaning_men_ids = fields.One2many('control.toilet_cleaning_men', 'sheet_id')
    groud_floor_office_adminitration_ids = fields.One2many('control.groud_floor_office_adminitration', 'sheet_id')
    groud_floor_offices_logistics_office_ids = fields.One2many('control.groud_floor_offices_logistics_office', 'sheet_id')
    groud_floor_office_cash_and_sales_department_ids = fields.One2many('control.groud_floor_office_cash_and_sales_department', 'sheet_id')
    temperature_of_freezers_ids = fields.One2many('control.temperature_of_freezers', 'sheet_id')
    first_floor_offices_area_ids = fields.One2many('control.first_floor_offices_area', 'sheet_id')


    @api.model
    def default_get(self, fields_list):
        """ Override default_get to prepopulate multiple One2many fields """
        res = super(ShopControlSheet, self).default_get(fields_list)
        
        # Predefined items for different One2many fields
        packing_room_items = [
            'Packing Production Report',
            'Packing Sticker Requirement',
            'Packing Plastic Requirement',
            'Hand Soap Lotion',
            'Cleanness of Flush',
            'Cleanness of Floor',
            'Presentation of Staff'
        ]
        
        toilet_cleaning_women_items = [
            'Tissue Paper In Toilet',
            'Spray In toilet',
            'Hand Soap Lotion',
            'Cleanness of Flush',
            'Cleanness of Floor',
            'Dusbin',
            'Cleaning Sheet',
            'Repairng If Any',
        ]
        
        toilet_cleaning_men_items = [
            'Tissue Paper In Toilet',
            'Spray In toilet',
            'Hand Soap Lotion',
            'Cleanness of Flush',
            'Cleanness of Floor',
            'Dusbin',
            'Cleaning Sheet',
            'Repairng If Any',
        ]
        
        groud_floor_office_adminitration_items = [
             'Cleaning of Floor and Desk',
                'Dusbins',
                'Toilets',
                'Cleaning Sheet',
        ]
        
        groud_floor_offices_logistics_office_items = ['Cleaning of Floor and Desk',
            'Dusbins',
            'Toilets',
            'Cleaning Sheet',]

        temperature_of_freezers_items = [
            'Frozen - Temperature Devise',
            'Warehouse Control Sheet',
            'Control Sheet Dated ',
            'Freezer - Temperature ',
            'Repairng If Any',
            'Temperature Monoring Sheet',
        ]
        first_floor_offices_area_items = [
            'Frozen - Temperature Devise',
            'Warehouse Control Sheet',
            'Control Sheet Dated ',
            'Freezer - Temperature ',
            'Repairng If Any',
            'Temperature Monoring Sheet',
        ]
        groud_floor_office_cash_and_sales_department_items = [
            'Frozen - Temperature Devise',
            'Warehouse Control Sheet',
            'Control Sheet Dated ',
            'Freezer - Temperature ',
            'Repairng If Any',
            'Temperature Monoring Sheet',
        ]
        # Create data for each One2many field
        packing_room_data = [(0, 0, {'item': item}) for item in packing_room_items]
        toilet_cleaning_women_data = [(0, 0, {'item': item}) for item in toilet_cleaning_women_items]
        toilet_cleaning_men_data = [(0, 0, {'item': item}) for item in toilet_cleaning_men_items]
        groud_floor_office_adminitration_data = [(0, 0, {'item': item}) for item in groud_floor_office_adminitration_items]
        groud_floor_offices_logistics_office_data = [(0, 0, {'item': item}) for item in groud_floor_offices_logistics_office_items]
        temperature_of_freezers_data = [(0, 0, {'item': item}) for item in temperature_of_freezers_items]
        first_floor_offices_area_data = [(0, 0, {'item': item}) for item in first_floor_offices_area_items]
        groud_floor_office_cash_and_sales_department_data = [(0, 0, {'item': item}) for item in groud_floor_office_cash_and_sales_department_items]
        # Update the result dictionary with prepopulated data
        res.update({
            'packing_room_ids': packing_room_data,
            'toilet_cleaning_women_ids': toilet_cleaning_women_data,
            'toilet_cleaning_men_ids': toilet_cleaning_men_data,
            'groud_floor_office_adminitration_ids': groud_floor_office_adminitration_data,
            'groud_floor_offices_logistics_office_ids': groud_floor_offices_logistics_office_data,
            'temperature_of_freezers_ids': temperature_of_freezers_data,
            'first_floor_offices_area_ids': first_floor_offices_area_data,
            'groud_floor_office_cash_and_sales_department_ids': groud_floor_office_cash_and_sales_department_data,
        })
        
        return res


class ToiletCleaning(models.Model):
    _name = 'control.packing_room'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)


class SaleArea(models.Model):
    _name = 'control.toilet_cleaning_women'
    _description = 'Sale Area'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)


class toilet_cleaning_men(models.Model):
    _name = 'control.toilet_cleaning_men'
    _description = 'toilet_cleaning_men'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)


class groud_floor_office_adminitration(models.Model):
    _name = 'control.groud_floor_office_adminitration'
    _description = 'groud_floor_office_adminitration'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)


class  TranslationOnProducts(models.Model):
    _name = 'control.groud_floor_offices_logistics_office'
    _description = 'Translation On Products'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)


class  GoodsMarket(models.Model):
    _name = 'control.groud_floor_office_cash_and_sales_department'
    _description = 'GoodsMarket'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)                

class  GoodsMarket(models.Model):
    _name = 'control.temperature_of_freezers'
    _description = 'GoodsMarket'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)         

class  GoodsMarket(models.Model):
    _name = 'control.first_floor_offices_area'
    _description = 'GoodsMarket'

    sheet_id = fields.Many2one('control.warehouse_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=False)            