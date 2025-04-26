# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity Withholding Tax',
    'version': "1.0.0",

    'summary': '',
    'author': 'Syed Subhan',
    'description': """""",
    'depends': ['account','base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_payment_register_view.xml',
        'views/views.xml',
          
        ],
   
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}



