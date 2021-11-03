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

#
#

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _sql_constraints = [
        ('_unique_one_sequence', 'unique (one_sequence)', "Sequence must be unique"),
    ]
    one_sequence = fields.Char(string='Sequence', readonly=True, store=True)
    partner_industry_id = fields.Many2one(comodel_name='res.partner.industry', related='partner_id.industry_id')
    partner_category_id = fields.Many2one(comodel_name='one.partner.category', related='partner_id.categ_id')
