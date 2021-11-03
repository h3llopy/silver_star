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

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [('partner_code', 'unique (partner_code)', "Code already Exist"),
                        ]

    categ_id = fields.Many2one(comodel_name='one.partner.category', string='Category')
    partner_code = fields.Char(string='Code')
    shipping_type = fields.Selection(selection=[('internal', 'Internal'), ('external', 'External')], default='internal')

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        res['industry_id'] = self.env['res.partner.industry'].search([('id', '=', 100)], limit=1).id
        return res


class ResPartnerCategory(models.Model):
    _name = 'one.partner.category'
    _sql_constraints = [('code', 'unique (code)', "Code already Exist"), ]

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    partner_ids = fields.One2many(comodel_name='res.partner', string='Partners', inverse_name='categ_id',domain="[('parent_id', '=', False)]")
    customers_count = fields.Integer(compute='compute_count')

    def get_customers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customers',
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain':[('parent_id', '=', False), ('categ_id','=',self.id)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        for record in self:
            record.customers_count = self.env['res.partner'].search_count(
                [('categ_id', '=', self.id)])

