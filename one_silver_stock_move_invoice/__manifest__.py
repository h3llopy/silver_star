
{
    'name': "one_silver_stock_move_invoice",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    'depends': ['stock', 'account'],
    'data': [
        'views/account_move_inherited.xml',
        'views/stock_picking_inherited.xml',
        'views/res_config_settings_inherited.xml',
        'wizard/picking_invoice_wizard.xml',
    ],
    'license': "AGPL-3",
    'images': ['static/description/banner.png'],
}
