# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity Fixed Asset Calculation',
    'version': "1.0.0",

    'summary': '',
    'description': """""",
    'depends': ['account','base','sale','account_asset','stock'],
    'data': [
          'security/ir.model.access.csv',
          'views/views.xml',
          
        ],
   
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}



