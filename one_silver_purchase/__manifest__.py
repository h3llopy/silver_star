# -*- coding: utf-8 -*-
{
    'name': "one_silver_purchase",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    'depends': ['base', 'purchase', 'purchase_stock', 'stock_landed_costs',
                'website_sale_stock', 'product_expiry'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_activity_data.xml',
        'views/res_partner.xml',
        'views/purchase_order.xml',
        'views/purchase_report.xml',
        'views/landed_cost.xml',
        'views/account_move.xml',
        'views/stock_move.xml',
    ],

}
