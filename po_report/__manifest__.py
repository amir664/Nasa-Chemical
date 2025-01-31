{
    'name': 'Purchase Order Report',
    'version': '17.0.1.0.0',

    'depends': ['base', 'purchase'],
    
    'data': ['wizard/wizard.xml',
             'report/report.xml',
             'report/report_template.xml',
             'security/ir.model.access.csv'
             ],
    
    'installable': True,
    'auto_install': False,
    'application': False,
}
