{
    'name': 'Sales Target Report',
    'version': '1.0.0',

    'depends': ['base','account','affinity_ext'],
    
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
