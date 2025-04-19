from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    record = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    name = fields.Date(string='Shop Control Dated')
    control_officer = fields.Char('res.users')
    control_officer3 = fields.Many2one('res.users',string='Control Officer Dated')
    toilet_cleaning_ids = fields.One2many('control.toilet_cleaning', 'sheet_id', string='Toilet Cleaning')
    sale_area_ids = fields.One2many('control.sale_area', 'sheet_id')
    freezer_ids = fields.One2many('control.freezer', 'sheet_id')
    staffing_ids = fields.One2many('control.staffing', 'sheet_id')
    translation_on_products_ids = fields.One2many('control.translation_on_products', 'sheet_id')
    goods_market_ids = fields.One2many('control.goods_market', 'sheet_id')


    def _check_all_tabs_filled(self):
        def validate_lines(lines, tab_name):
            for line in lines:
                if not line.yes_no:
                    raise UserError(_("The tab '%s' is not fully filled. Please complete all required fields.") % tab_name)

        validate_lines(self.toilet_cleaning_ids, "Toilet Cleaning")
        validate_lines(self.sale_area_ids, "Sale Area")
        validate_lines(self.freezer_ids, "Freezer")
        validate_lines(self.staffing_ids, "Staffing")
        validate_lines(self.translation_on_products_ids, "Translation On Products")
        validate_lines(self.goods_market_ids, "Goods Market")


    @api.model
    def create(self, vals):
        if vals.get('record', 'New') == 'New':
            vals['record'] = self.env['ir.sequence'].next_by_code('control.shop_control_sheet') or 'New'
        record = super().create(vals)
        record._check_all_tabs_filled()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._check_all_tabs_filled()
        return res
    



    @api.model
    def default_get(self, fields_list):
        """ Override default_get to prepopulate multiple One2many fields """
        res = super(ShopControlSheet, self).default_get(fields_list)
        
        # Predefined items for different One2many fields
        toilet_cleaning_items = [
            'Tissue Paper In Toilet',
            'Spray In Toilet',
            'Hand Soap Lotion',
            'Cleanness of Flush',
            'Cleanness of Floor',
            'Dusbin',
        ]
        
        sale_area_items = [
            'Invoices and Sales File',
 'Cleaning of Floor',
 'Counter Area',
 'First Aid Box',
 'Shop Registration Form',
 'Missing Stock of Master Business Products',
 'Cleaning of Racks',
 'Aldi, Colyrupt and Mns Stocks',
        ]
        
        freezer_items = [
             'Frozen Goods -  Temperature Devise',
 'Freezer - Temperature Monitoring Devise',
 'Temperature of Freezer',
        ]
        
        staffing_items = [
             'Late Staff / Absent Staff',
 'Staff Work Contracts',
 'Staff Medical Report',
 'Presentation',
        ]
        
        translation_on_products_items = []
        
        # Create data for each One2many field
        toilet_cleaning_data = [(0, 0, {'item': item}) for item in toilet_cleaning_items]
        sale_area_data = [(0, 0, {'item': item}) for item in sale_area_items]
        freezer_data = [(0, 0, {'item': item}) for item in freezer_items]
        staffing_data = [(0, 0, {'item': item}) for item in staffing_items]
        translation_on_products_data = [(0, 0, {'item': item}) for item in translation_on_products_items]
        
        # Update the result dictionary with prepopulated data
        res.update({
            'toilet_cleaning_ids': toilet_cleaning_data,
            'sale_area_ids': sale_area_data,
            'freezer_ids': freezer_data,
            'staffing_ids': staffing_data,
            'translation_on_products_ids': translation_on_products_data,
        })
        
        return res


class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)
    attachment = fields.Binary(string='Attachment', attachment=True)


class SaleArea(models.Model):
    _name = 'control.sale_area'
    _description = 'Sale Area'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)
    attachment = fields.Binary(string='Attachment', attachment=True)


class Freezer(models.Model):
    _name = 'control.freezer'
    _description = 'Freezer'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)
    attachment = fields.Binary(string='Attachment', attachment=True)


class Staffing(models.Model):
    _name = 'control.staffing'
    _description = 'Staffing'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)
    attachment = fields.Binary(string='Attachment', attachment=True)


class  TranslationOnProducts(models.Model):
    _name = 'control.translation_on_products'
    _description = 'Translation On Products'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)
    attachment = fields.Binary(string='Attachment', attachment=True)


class  GoodsMarket(models.Model):
    _name = 'control.goods_market'
    _description = 'GoodsMarket'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(string='Item', readonly=True)  # 'readonly=True' ensures this field cannot be edited
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks', required=False)                
    attachment = fields.Binary(string='Attachment', attachment=True)