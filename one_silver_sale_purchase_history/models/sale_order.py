# -*- coding: utf-8 -*-


#  One Solution
#  -----------------------
#  @author :ibralsmn.
#  @mailto : ibralsmn@onesolutionc.com.
#  @company : onesolutionc.com.
#  @project : international_center.
#  @module:  addons.
#  @file : model.py.
#  @created : 9/30/21, 3:39 PM.
#


from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def one_get_product_history_data(self):
        values = []
        customer_id = self.order_id.partner_id
        customer_order = self.env['sale.order'].search(
            [('partner_id', '=', customer_id.id), ('state', 'in', ('sale', 'done'))])
        for order in customer_order:
            for line in order.order_line:
                if line.product_id == self.product_id:
                    values.append((0, 0, {'sale_order_id': order.id,
                                          'sale_order_line_id': line.id,
                                          'history_price': line.price_unit,
                                          'history_qty': line.product_uom_qty,
                                          'history_total': order.amount_total
                                          }))
        history_id = self.env['product.sale.order.history'].create({
            'product_id': self.product_id.id,
            'product_sale_history': values
        })

        return {
            'name': 'Customer Product Sales History',
            'view_mode': 'form',
            'res_model': 'product.sale.order.history',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': history_id.id
        }
