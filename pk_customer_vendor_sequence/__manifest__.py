# -*- coding: utf-8 -*-

{
    'name': "Customer Vendor Sequence Number",
    "version": "17.0.0.1",
    'author': 'Irfan Ullah',
    'website': 'https://www.youtube.com/@irfanullah',
    'summary': 'Sequence number for Customer and Vendor',
    'license': 'LGPL-3',
    "description": """This module generate sequence number for customer and vendor.""",
    'depends': ['base', 'sale_management', 'purchase'],
    'data': [
        'data/sequence.xml',
        'views/res_partner.xml',
    ],
    'images': ['static/description/banner.png'],
    "auto_install": False,
    "installable": True,

}
