# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import yaml

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
import odoo

from werkzeug.exceptions import Forbidden

_logger = logging.getLogger(__name__)


class PowerBIController(http.Controller):
    _return_url = "/powerbi/connect"

    @http.route(
        _return_url, type='json', auth='public', methods=['POST'], csrf=False,
        save_session=False
    )
    def retrieve(self, **data):
        verify_token = request.env['ir.config_parameter'].sudo().get_param('powerbi.verify_token')
        token = data.get('verify_token')
        model_name = data.get('model')
        
        if token != verify_token:
            raise Forbidden()
        
        logging.info(data)
        logging.info(model_name)
        #search based on model name
        records = request.env[model_name].sudo().search([])
        # records = request.env[model_name].sudo().browse(records)
        
        all_fields = request.env[model_name].fields_get()
        field_names = list(all_fields.keys())
        
        result = records.sudo().read(fields=field_names)
        # result = []
        
        # for record in records:
        #     row = {}
        #     # for field in all_fields:
        #     #     row[field] = record[field]
        #     result.append(record.sudo().read(fields=field_names))
            
            
        # all_fields = request.env[model_name].fields_get()
        # field_names = list(all_fields.keys())
            
        # records = records.sudo().read(fields=field_names)
        logging.info(records)
            
        return result
    