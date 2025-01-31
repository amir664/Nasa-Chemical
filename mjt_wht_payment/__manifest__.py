{
    'name': "Payment WHT",

    'summary': """
        Extend Payment usage""",

    'description': """
    """,
    'author': "MJT",
    'license':'AGPL-3',
    # 'website': "http://www.metrocomjaddi.com",
    'category': 'Accounting',
    'version' : '1.0.0',

    'depends': ['account'],

    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
        'views/bukti_potong_view.xml',
    ],
}
