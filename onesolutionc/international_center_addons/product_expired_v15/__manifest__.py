{
    'name': 'Product Expiration',


    'author': 'Ezz Eldin Saleh',

    'depends': ['base','stock','sale_management','mail','product_expiry','product'],
    'data': ['views/cron_jop.xml',
             'views/view_expiry_in_lot.xml',
             'security/group.xml',
                     ],


}