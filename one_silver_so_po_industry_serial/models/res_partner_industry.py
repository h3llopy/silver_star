#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

from odoo import fields, models


class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'
    _sql_constraints = [('code', 'unique (code)', "Code already Exist"), ]

    parent_id = fields.Many2one(comodel_name='res.partner.industry', string='Parent')
    code = fields.Char(string='Code')
