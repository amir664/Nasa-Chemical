{
    'name': 'Sales Report',
    'version': '1.0.0',

    'depends': ['base'],
    
    'data': [
            'security/ir.model.access.csv',
            'wizard/wizard.xml',
            'report/report.xml',
            'report/report_template.xml',
],
    

    'installable': True,
    'auto_install': False,
    'application': False,
}
