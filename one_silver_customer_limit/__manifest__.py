# -*- coding: utf-8 -*-
{
    'name': "one_silver_customer_limit",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    'depends': ['base','sale','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/warning_wizard.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
}
