
{
    'name': 'Check Management',
    'category': 'Accounting',
    'summary': 'Issuing and receiving check for payment account',
    'version': '15.0.0.1',
    'description': """Check  Management """,
    'author': 'Ahmed Amen',
    'depends': ['account','account_payment',],
    'data': [
        'security/account_check_payment_security.xml',
        'security/ir.model.access.csv',
        'views/account_journal_inherit_view.xml',
        'views/payment_view.xml',
        'views/check_payment_views.xml',
        # 'views/check_folder.xml',
        'views/server_actions.xml',
        # 'views/print_payment_cash.xml',
        'views/check_payment_transaction_payment_views.xml',
        'wizard/endorse_wizard.xml',
        'wizard/action_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
