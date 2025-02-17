from odoo import api , fields , models,_
from odoo.exceptions import UserError


class ShipmentModel(models.Model):
    _name = "shipment.model"
    _description = "Shipment Model"
    _rec_name = "shipping_name"


    shipping_name = fields.Char(string="Shipping Name",required=True,copy=False,default=lambda self: _('New'))
    shipment_date = fields.Date(string="Shipment Date")
    analytic_account_id =fields.Many2one('account.analytic.account',string="Analytic Account")
    # order_no = fields.Char(string="Order No")
    port_of_origin = fields.Char(string="Port Of Origin")
    port_of_destination = fields.Char(string="Port Of Destination")
    # shipment_no = fields.Char(string="Shipment No")
    invoice_no = fields.Char(string="Invoice No.")
    # shipment_company_name = fields.Char(string="Shipment Company Name")
    # bl_no = fields.Char(string="B/L")
    eta_date = fields.Date(string="ETA")
    etd_date = fields.Date(string="ETD")
    state = fields.Selection([('schedule','Schedule'),('at origin','At Origin'),('in transit','In Transit'),('at port','At Port')],string="State")
    # dimension = fields.Char(string="Dimension")
    # weight = fields.Integer(string="Weight")

    # etd_date = fields.Date(string="Expected Time Of Delivery")