# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Shipping Model',
    'version': '1.2',  
    'category': '',
    'sequence' : -1,
    'summary': '',
    'description': """""",
    # ,'purchase_request','purchase','stock','stock_landed_costs'
    'depends': ['base','base_setup','analytic'],
    'demo': [],
    'data':[
        'security/ir.model.access.csv',
        # 'data/customer_sequence.xml',
        # 'views/affinity_ext.xml',
        'views/shipping_model.xml',
        'views/letter_credit.xml',
        'views/lc_processing.xml',
        'views/ext.xml',
        

    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         'nwlc_crm_ext/static/src/**',
    #     ],
       
    # },
    'application':True,
    'installable': True,
    'auto_install':False,
    'license': 'LGPL-3',
}
