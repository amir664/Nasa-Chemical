# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountTax(models.Model):
    _inherit = "account.tax"

    withholding_tax = fields.Boolean(string="Withholding Tax")
    basic_tax = fields.Boolean(string="Basic Tax",default=True)
    with_sales_tax = fields.Boolean(string="With Sales Tax")
