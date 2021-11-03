# -*- coding: utf-8 -*-
{
    'name': "one_silver_attachment_and_document",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    'depends': ['base', 'documents', 'sale', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/document.xml',
        'views/ir_attachment.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
    ],

}
