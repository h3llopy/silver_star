from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def one_get_product_history_data(self):
        values = []
        vendor_id = self.order_id.partner_id
        vendor_order = self.env['purchase.order'].search(
            [('partner_id', '=', vendor_id.id), ('state', 'not in', ('draft','sent','to approve', 'cancel'))])

        for order in vendor_order:
            for line in order.order_line:
                if line.product_id == self.product_id:
                    values.append((0, 0, {'purchase_order_id': order.id,
                                          'purchase_order_line_id': line.id,
                                          'history_price': line.price_unit,
                                          'history_qty': line.product_uom_qty,
                                          'history_total': order.amount_total
                                          }))
        history_id = self.env['product.purchase.order.history'].create({
            'product_id': self.product_id.id,
            'product_purchase_history': values
        })

        return {
            'name': 'Vendor Product Purchase History',
            'view_mode': 'form',
            'res_model': 'product.purchase.order.history',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': history_id.id
        }