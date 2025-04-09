{
    'name': 'Nofification App',
    'version': '1.0',
    'summary': 'App with ir.model and ir.model.fields form',
    'category': 'Custom',
    'author': 'Asfiyan Shivani',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
    ],
    'installable': True,
    'application': True,
}
