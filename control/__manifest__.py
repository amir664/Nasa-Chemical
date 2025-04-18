{
    'name': 'Control',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Control App for Shop',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',        
        'views/shop_control_sheet_views.xml',
        'views/warehouse_control_sheet_views.xml',
        'views/control_menus.xml'
    ],
    'installable': True,
}
