{
    'name': 'Control',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Control App for Shop',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/control_menus.xml',
        'views/shop_control_sheet_views.xml',
    ],
    'installable': True,
}
