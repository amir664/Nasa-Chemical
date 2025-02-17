from odoo import api , fields , models,_
from odoo.exceptions import UserError


class LetterCredit(models.Model):
    _name = "lc.processing.release.detail"
    _description = "LC Processiong And Release Details"
    _rec_name = "name"


    name = fields.Char(string="Name",required=True,copy=False,default=lambda self: _('New'))
    lc_id =fields.Many2one('letter.of.credit',string="LC No.")
    lc_request_date = fields.Date(string="LC Request Date")
    doc_submission_date = fields.Date(string="Document Submission Date")
    shipment_date = fields.Date(string="Shipment Date")
    payment_date = fields.Date(string="Payment Date")
    submission_date = fields.Date(string="Submission Date")
    doc_revision_date = fields.Date(string="Document Revision Date")
    doc_recieved_date = fields.Date(string="Document Recieved Date")
    bill_landing_no = fields.Char(string="Bill Of Landing No.")
    # currency_id =fields.Many2one('res.currency',string="Currency")
    # issuance_date = fields.Date(string="Issuance Date")
    # lc_amount = fields.Float(string="LC Amount")
    # lc_type = fields.Selection([('sight','Sight'),('usance','Usance')],string="LC Type")
    # state = fields.Selection([('draft','Draft'),('received','Received')],string="State")