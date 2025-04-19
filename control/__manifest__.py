{
    'name': 'Control',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Control App for Shop',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',        
        'data/toilet_cleaning_sequence.xml',
        'views/shop_control_sheet_views.xml',
        'views/warehouse_control_sheet_views.xml',
        'views/control_menus.xml'
    ],
    'installable': True,
}
