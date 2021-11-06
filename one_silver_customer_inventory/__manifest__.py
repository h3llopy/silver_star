# -*- coding: utf-8 -*-
{
    'name': "one_silver_customer_inventory",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','uom','sale','one_silver_customer_target'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/customer_inventory.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
