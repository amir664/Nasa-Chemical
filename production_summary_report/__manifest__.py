{
    'name': 'Production Summary Report',
    'version': '17.0.1.0.0',

    'depends': ['mrp', 'stock'],
    
    'data': ['wizard/wizard.xml',
            #  'report/report.xml',
            #  'report/report_template.xml',
             'security/ir.model.access.csv'
             ],
    
    'installable': True,
    'auto_install': False,
    'application': True,
}
