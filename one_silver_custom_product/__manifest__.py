#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / __manifest__.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# -*- coding: utf-8 -*-
{
    'name': "one_silver_custom_product",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale','one_silver_free_products'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/product.xml',
        'views/sales_order.xml',
        'views/product_reports.xml',
        'views/product_product_templates.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
