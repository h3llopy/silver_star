#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / product.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.template'
    allow_free = fields.Boolean(string='Allow Be Free', default=False)
    free_types_allowed = fields.Many2many(comodel_name='one.free.type', string='Allowed Free Types',
                                          relation='product_product_free_types_rel')
