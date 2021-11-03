#  One Solution
#  -----------------------
#  @author :ibralsmn.
#  @mailto : ibralsmn@onesolutionc.com.
#  @company : onesolutionc.com.
#  @project : international_center.
#  @module:  addons.
#  @file : __manifest__.py.
#  @created : 9/30/21, 3:39 PM.
#

{
    'name': "one_silver_sale_purchase_history",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    'depends': ['base', 'sale_management', 'one_silver_so_po_industry_serial','sale_margin','one_silver_purchase_discount'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'wizard/sales_order_history_wizard_view.xml',
        'views/purchase_order.xml',
        'wizard/purchase_order_history_wizard_view.xml',
        'views/view.xml',
    ],
    'images': ['static/description/banner.png'],

}
