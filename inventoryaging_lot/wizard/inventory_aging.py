from odoo import _, api, fields, models
from odoo.exceptions import UserError
import datetime



class InventoryAgingWizard(models.TransientModel):
    _name = 'inventoryaging.lot'
    _description = 'Lot Wise Inventory Aging'


    product_ids=fields.Many2many('product.product',string='Products')
    date_from = fields.Datetime('Date Form')
    date_to = fields.Datetime('Date To')
    category_ids=fields.Many2many('product.category',string='Product Categories')
    location_ids=fields.Many2many('stock.location',string='Locations')
    lot_ids=fields.Many2many('stock.lot',string='Lots/Serial')
    

    def generate_report(self):

        product_ids = []
        if self.product_ids:
            for id in self.product_ids:
                product_ids.append(id.id)

        category_ids = []
        if self.category_ids:
            for id in self.category_ids:
                category_ids.append(id.id)

        location_ids = []
        if self.location_ids:
            for id in self.location_ids:
                location_ids.append(id.id)

        lot_ids = []
        if self.lot_ids:
            for id in self.lot_ids:
                lot_ids.append(id.id)

        # product_ids = self.product_ids.ids
        # category_ids = self.category_ids.ids
        # location_ids = self.location_ids.ids
        # lot_ids = self.lot_ids.ids
        date_to = self.date_to if self.date_to else datetime.datetime.today()
        # raise UserError(date_to)
        # date_to = datetime.datetime.today()
        # if self.date_to:
        #     date_to = self.date_to + datetime.timedelta(days=1) 
        date_from = self.date_from if self.date_from else '01-01-2000 00:00:00'
        return {
        'type': 'ir.actions.act_url',
        'url': '/inventoryaging_lot/excel?product_ids=%s&category_ids=%s&location_ids=%s&lot_ids=%s&date_from=%s&date_to=%s' % (
            product_ids, 
            category_ids, 
            location_ids,
            lot_ids,
            date_from, date_to,
        ),
        'target': 'self',
        }