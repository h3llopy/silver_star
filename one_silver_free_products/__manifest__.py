
{
    'name': "one_silver_free_products",
    'description': """ """,
    'summary': '',
    'author': "One Solution",
    'website': "http://www.onescolutionc.com",
    'category': '',
    'version': '1',
    'sequence': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/free_type.xml',
        'views/res_partner.xml',
        'views/sales_order.xml',
        'views/product.xml',
        'views/res_users.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
