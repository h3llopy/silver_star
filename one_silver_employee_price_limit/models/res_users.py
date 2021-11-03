#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / res_users.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    user_limit_type = fields.Selection(string="User Limit Type",
                                       selection=[('user_limit', 'User Limit'), ('product_limit', 'Product limit')],
                                       default='product_limit', required=True)
