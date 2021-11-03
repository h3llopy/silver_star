# -*- coding: utf-8 -*-
{
    'name': "One Nagm Sale Reports",
    'description': """ """,
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': 'Sales',
    'version': '15.0.1.0.0',
    'sequence': '1',
    'depends': ['base', 'sale', 'product',
                'one_silver_so_po_industry_serial'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'report/forward_sale_template.xml',
        'report/sultan_center_template.xml',
        'report/forward_invoice_template.xml',
        'report/sultan_invoice_template.xml',
        'report/order_quotation_template.xml',
        'report/print_label_template.xml',
        'report/product_template.xml',
        'report/product_report.xml',
        'report/sale_report.xml',
        'report/account_move.xml',
    ],

}
