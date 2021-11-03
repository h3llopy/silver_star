#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / sale_order.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def confirm_order_server_action(self):
        for record in self:
            if record.state in ['draft', 'sent', 'approve'] and record.can_confirm == True:
                record.one_sequence = self.env['one.sequence'].next_one_sequence(used_for='sale', partner_id=record.partner_id)
                record.action_confirm()
            else:
                raise ValidationError('can\'t Confirm Sales Order')

    def create_order_server_action(self):
        for record in self:
            delivered = True
            for line in record.order_line:
                if line.product_uom_qty != line.qty_delivered:
                    delivered = False
            if delivered:
                record._create_invoices()
            else:
                raise ValidationError('The Sale Order is Not Delivered.')
