from odoo import models, fields, api, _
from odoo.exceptions import UserErro


class ShopControlSheet(models.Model):
    _name = 'control.shop_control_sheet'
    _description = 'Shop Control Sheet'

    name = fields.Date(string='Shop Control Dated', required=True)
    control_officer = fields.Char(string='Control Officer', required=True)
    toilet_cleaning_ids = fields.One2many('control.toilet_cleaning', 'sheet_id', string='Toilet Cleaning')

    @api.model
    def create(self, vals):
        # Auto-fill checklist items if not manually added
        if not vals.get('toilet_cleaning_ids'):
            checklist_items = [
                'Tissue Paper In Toilet',
                'Soap Available',
                'Toilet Floor Clean',
                'Dustbin Available',
                'Hand Dryer Working',
            ]
            vals['toilet_cleaning_ids'] = [(0, 0, {'item': item}) for item in checklist_items]

        return super().create(vals)

    def write(self, vals):
        # Also check for required fields before update
        res = super().write(vals)
        for rec in self:
            for line in rec.toilet_cleaning_ids:
                if not all([line.yes_no, line.condition, line.remarks]):
                    raise UserError(_("Please fill all fields in the Toilet Cleaning checklist."))
        return res


class ToiletCleaning(models.Model):
    _name = 'control.toilet_cleaning'
    _description = 'Toilet Cleaning Checklist'

    sheet_id = fields.Many2one('control.shop_control_sheet', string='Control Sheet')
    item = fields.Char(readonly=True)
    yes_no = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Yes/No', required=True)
    condition = fields.Selection([('good', 'Good'), ('bad', 'Bad')], string='Condition', required=True)
    remarks = fields.Text(string='Remarks', required=True)
