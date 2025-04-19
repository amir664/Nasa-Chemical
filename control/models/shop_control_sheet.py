from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Shop Control Dated')
    control_officer = fields.Char('res.users')
    control_officer3 = fields.Many2one('res.users', string='Control Officer Dated')

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
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('control.shop_control_sheet') or 'New'
        record = super().create(vals)
        record._check_all_tabs_filled()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._check_all_tabs_filled()
        return res


class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([
        ('tissue', 'Tissue Paper In Toilet'),
        ('spray', 'Spray In Toilet'),
        ('soap', 'Hand Soap Lotion'),
        ('flush', 'Cleanness of Flush'),
        ('floor', 'Cleanness of Floor'),
        ('dusbin', 'Dusbin')
    ], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)


class SaleArea(models.Model):
    _name = 'control.sale_area'
    _description = 'Sale Area'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([
        ('invoices', 'Invoices and Sales File'),
        ('floor_clean', 'Cleaning of Floor'),
        ('counter', 'Counter Area'),
        ('first_aid', 'First Aid Box'),
        ('registration', 'Shop Registration Form'),
        ('missing_stock', 'Missing Stock of Master Business Products'),
        ('rack_cleaning', 'Cleaning of Racks'),
        ('aldi_stock', 'Aldi, Colyrupt and Mns Stocks')
    ], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)


class Freezer(models.Model):
    _name = 'control.freezer'
    _description = 'Freezer'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([
        ('frozen_goods', 'Frozen Goods -  Temperature Devise'),
        ('monitoring_device', 'Freezer - Temperature Monitoring Devise'),
        ('temperature', 'Temperature of Freezer')
    ], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)


class Staffing(models.Model):
    _name = 'control.staffing'
    _description = 'Staffing'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([
        ('late_absent', 'Late Staff / Absent Staff'),
        ('contracts', 'Staff Work Contracts'),
        ('medical', 'Staff Medical Report'),
        ('presentation', 'Presentation')
    ], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)


class TranslationOnProducts(models.Model):
    _name = 'control.translation_on_products'
    _description = 'Translation On Products'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)


class GoodsMarket(models.Model):
    _name = 'control.goods_market'
    _description = 'Goods Market'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Selection([], string='Item')
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No')
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment', attachment=True)
