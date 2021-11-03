{
    'name': "one_silver_customer_target",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','sales_team', 'uom'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/crm_team_views.xml',
        'views/res_partner.xml',
        'views/customer_target.xml',
        'views/sale_order.xml',
        'views/hr_employee.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
