#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / sales_order.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, api


class SalesOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _domain_invoice_delivery_address(self):
        return {
            'domain': {
                'partner_invoice_id': "[('parent_id','=',%s),'|', ('company_id', '=', False), ('company_id', '=', company_id)]" % self.partner_id.id,
                'partner_shipping_id': "[('parent_id','=',%s),'|', ('company_id', '=', False), ('company_id', '=', company_id)]" % self.partner_id.id
            }
        }


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('partner_id')
    def _domain_invoice_delivery_address(self):
        return {
            'domain': {
                'partner_shipping_id': "[('parent_id','=',%s),'|', ('company_id', '=', False), ('company_id', '=', company_id)]" % self.partner_id.id
            }
        }
