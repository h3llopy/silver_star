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
            lang = self.env.user.lang
            return num2words(amount, lang=lang)

    def print_report(self):
        """ Print Report """
        if self.report_template_id:
            data = {
                'inv_id': self.id,
            }
            return (
                self.report_template_id.report_action(self, data=data)
            )
