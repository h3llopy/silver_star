#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

#
#

# -*- coding: utf-8 -*-
{
    'name': "one_silver_so_po_industry_serial",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'stock', 'purchase', 'contacts'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/one_sequence.xml',
        'views/sales_order.xml',
        'views/purchase_order.xml',
        'views/res_partner_industry.xml',
        'views/res_partner.xml',
        'views/stock_picking.xml',
        'views/account_move.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
