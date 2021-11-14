""" Initialize Account Move """

from num2words import num2words
from odoo import fields, models


class AccountMove(models.Model):
    """
        Inherit Account Move:
         -
    """
    _inherit = 'account.move'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order'
    )

    report_template_id = fields.Many2one(
        related='partner_id.inv_report_id'
    )

    def _get_total_with_user_lang(self, amount):
        """ Get Total With User Lang """
        if amount != 0:
            lang = self.partner_id.lang
            return num2words(amount, lang=lang)

    def print_report(self):
        """ Print Report """
        if self.sale_id:
            if self.report_template_id:
                return (
                    self.report_template_id.report_action(self.sale_id)
                )
            else:
                return (
                    self.env.ref('sale.action_report_saleorder').report_action(self)
                )
