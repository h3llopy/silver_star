""" Initialize Sale Order """

from num2words import num2words
from odoo import api, fields, models


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         - 
    """
    _inherit = 'sale.order'

    purchase_order_id = fields.Many2one(
        'purchase.order', string='Purchase Order Ref'
    )
    report_template_id = fields.Many2one(
        related='partner_id.sale_report_id'
    )
    partner_commission = fields.Float(related='partner_id.partner_commission')
    partner_commission_value = fields.Float(
        compute='_compute_partner_commission_value', store='1')

    @api.depends('partner_commission', 'partner_commission')
    def _compute_partner_commission_value(self):
        """ Compute partner_commission_value value """
        for rec in self:
            if rec.amount_total:
                rec.partner_commission_value = (
                                                       rec.amount_total * rec.partner_commission) / 100

    def _get_total_with_user_lang(self, amount):
        """ Get Total With User Lang """
        if amount != 0:
            lang = self.env.user.lang
            return num2words(amount, lang=lang)

    def print_report(self):
        """ Print Report """
        if self.report_template_id:
            data = {
                'order_id': self.id,
            }
            return (
                self.report_template_id.report_action(self, data=data)
            )

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({'sale_id': self.id})
        return res
