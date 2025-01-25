{
    'name':'Customer Target Report',
    'version':'17.0.1.0.0',
    'depends': ['base','contacts'],
    'data':[
        'wizard/wizard.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        # 'report/report_template.xml'
    ],
    'installable':True,
    'auto-install':False,
    'application':False
}