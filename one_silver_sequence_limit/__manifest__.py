#  /**
#   * @author :ibralsmn
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : international_center
#   * @module:  addons
#   * @file : __manifest__.py
#   * @created : 9/30/21, 3:25 PM
#
#  **/

# -*- coding: utf-8 -*-
{
    'name': "one_silver_sequence_limit",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'one_silver_employee_price_limit', 'one_silver_so_po_industry_serial'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
