#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/


from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    _sql_constraints = [
        ('_unique_one_sequence', 'unique (one_sequence)', "Sequence must be unique"),
    ]
    one_sequence = fields.Char(string='Sequence', readonly=True, store=True)
    partner_industry_id = fields.Many2one(comodel_name='res.partner.industry', related='partner_id.industry_id')
    partner_category_id = fields.Many2one(comodel_name='one.partner.category', related='partner_id.categ_id')


    def button_confirm(self):
        for order in self:
            order.one_sequence = self.env['one.sequence'].next_one_sequence(used_for='purchase', partner_id=order.partner_id)
            res = super(PurchaseOrder, self).button_confirm()
        return True

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        vb = self.env['account.move'].browse(res['res_id'])
        vb.one_purchase_id = self.id
        vb.one_sequence = self.one_sequence
        return res