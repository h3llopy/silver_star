#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / product.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_list_price = fields.Float(string='Min Sales Price')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    min_list_price = fields.Float(string='Min Sales Price')
