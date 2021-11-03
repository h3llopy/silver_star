#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / account_move.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sales_order_id = fields.Many2one(comodel_name="sale.order",  string="Sale Order", readonly=1)
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address',
                                          related='sales_order_id.partner_shipping_id', )
