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
                    raise UserError(_("The tab '%s' is not fully filled. Please complete all required fields." % tab_name))

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

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        if 'toilet_cleaning_ids' in fields_list:
            res['toilet_cleaning_ids'] = [
                (0, 0, {'item': 'Tissue Paper In Toilet','yes_no': 'no'}),
                (0, 0, {'item': 'Spray In Toilet', 'yes_no': 'no'}),
                (0, 0, {'item': 'Hand Soap Lotion', 'yes_no': 'no'}),
                (0, 0, {'item': 'Cleanness of Flush', 'yes_no': 'no'}),
                (0, 0, {'item': 'Cleanness of Floor', 'yes_no': 'no'}),
                (0, 0, {'item': 'Dusbin', 'yes_no': 'no'}),
            ]

        if 'freezer_ids' in fields_list:
            res['freezer_ids'] = [
                (0, 0, {'item': 'Frozen Goods -  Temperature Devise','yes_no': 'no'}),
                (0, 0, {'item': 'Freezer - Temperature Monitoring Devise', 'yes_no': 'no'}),
                (0, 0, {'item': 'Temperature of Freezer', 'yes_no': 'no'})
            ]

        if 'sale_area_ids' in fields_list:
            res['sale_area_ids'] = [
                (0, 0, {'item': 'Invoices and Sales File', 'yes_no': 'no'}),
                (0, 0, {'item': 'Cleaning of Floor', 'yes_no': 'no'}),
                (0, 0, {'item': 'Counter Area', 'yes_no': 'no'}),
                (0, 0, {'item': 'First Aid Box', 'yes_no': 'no'}),
                (0, 0, {'item': 'Shop Registration Form', 'yes_no': 'no'}),
                (0, 0, {'item': 'Missing Stock of Master Business Products', 'yes_no': 'no'}),
                (0, 0, {'item': 'Cleaning of Racks', 'yes_no': 'no'}),
                (0, 0, {'item': 'Aldi, Colyrupt and Mns Stocks', 'yes_no': 'no'})
            ]

        if 'staffing_ids' in fields_list:
            res['staffing_ids'] = [
                (0, 0, {'item': 'Late Staff / Absent Staff', 'yes_no': 'no'}),
                (0, 0, {'item': 'Staff Work Contracts', 'yes_no': 'no'}),
                (0, 0, {'item': 'Staff Medical Report', 'yes_no': 'no'}),
                (0, 0, {'item': 'Presentation', 'yes_no': 'no'})
            ]

        if 'translation_on_products_ids' in fields_list:
            res['translation_on_products_ids'] = []

        if 'goods_market_ids' in fields_list:
            res['goods_market_ids'] = []

        return res