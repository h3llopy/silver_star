""" Initialize Sale Order """

from num2words import num2words

from odoo import fields, models


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

    def _get_total_with_user_lang(self, amount):
        """ Get Total With User Lang """
        if amount != 0:
            lang = self.env.user.lang
            return num2words(amount, lang=lang)

    def get_delivery_address(self, partner_shipping):
        """ Get Delivery Address """
        if partner_shipping:
            record = self.env['res.partner'].search(
                [('id', '=', partner_shipping)])
            address = ""
            if record.street:
                address += record.street
            if record.street2:
                address += " " + record.street2
            if record.city:
                address += " " + record.city
            if record.state_id:
                address += " " + record.state_id.name
            if record.zip:
                address += " " + record.zip
            if record.country_id:
                address += " " + record.country_id.name
            return address

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
