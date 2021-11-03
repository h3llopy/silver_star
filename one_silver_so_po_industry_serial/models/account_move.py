#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/


from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    one_purchase_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
    one_sale_id = fields.Many2one(comodel_name='sale.order', string='Sales Order')
    one_sequence = fields.Char(string='Sequence',store=True, readonly=True)

