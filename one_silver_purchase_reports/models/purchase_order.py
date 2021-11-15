""" Initialize Purchase Order """
import num2words as num2words

from odoo import fields, models


class PurchaseOrder(models.Model):
    """
        Inherit Purchase Order:
         -
    """
    _inherit = 'purchase.order'

    # def _prepare_invoice(self):
    #     res = super(PurchaseOrder, self)._prepare_invoice()
    #     res.update({'one_sequence': self.one_sequence})

    delivery_schedule = fields.Char()
    sale_ref = fields.Char()
    sale_date = fields.Date()
    #
    def _get_total_with_user_lang(self, amount, lang):
        """ Get Total With User Lang """
        if amount != 0:
            # lang = self.env.user.lang
            return num2words(number=amount, lang=lang, to='currency')
