# -*- coding: utf-8 -*-
{
    'name': 'Customer Target App',
    'author': 'Syed Subhan , Muhammad Osama',
    'version': '17.0.1.1',
    'description': """Customer Target App""",
    'depends': [ 'base'],
    'data': [
        'views/customer_target.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}