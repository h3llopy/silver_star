#  /**
#   * @author :ibralsmn
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : international_center
#   * @module:  addons
#   * @file : sale_order.py
#   * @created : 9/30/21, 3:25 PM
#
#  **/

#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

#
#

from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def next_sales_order_action(self):
        if self.order_line:
            if self.order_line.search(
                    [('need_approve', '=', True), ('approve_done', '=', False), ('is_free', '=', False),
                     ('order_id', '=', self.id)]):
                for record in self.order_line:
                    if record.need_approve:
                        self.env['one.sale.order.line.need.approve'].create({
                            'sale_order_id': record.order_id.id,
                            'sale_order_line_id': record.id,
                            'product_id': record.product_id.id,
                            'state': 'new',
                            'final_amount': record.price_unit,
                            'need_approve_price_unit': record.price_unit if self.user_limit_method == 'amount' or self.user_limit_type == 'product_limit' else False,
                            'need_approve_percent': record.discount if self.user_limit_method == 'percent' else False

                        })
                self.state = 'need_approve'
            else:
                self.one_sequence = self.env['one.sequence'].next_one_sequence(used_for='sale', partner_id=self.partner_id)
                return super(SaleOrder, self).with_context(default_sale_id=self.id).action_confirm()
        else:
            raise ValidationError('You can\'t go next without lines')
