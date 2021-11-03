#  One Solution
#
#  @author :ibralsmn.
#  @mailto : ibralsmn@onesolutionc.com.
#  @company : onesolutionc.com.
#  @project : international_center.
#  @module:  addons.
#  @file : landed_cost.py.
#  @created : 10/9/21, 1:28 PM.
#

from odoo import fields, models, api


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    purchase_orders_count = fields.Integer()

    def get_related_purchase_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'view_mode': 'tree',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', self.picking_ids.purchase_id.ids)],
            'context': "{'create': False}"
        }