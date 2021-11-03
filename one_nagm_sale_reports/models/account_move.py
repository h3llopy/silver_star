""" Initialize Account Move """

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
                'inv_id': self.id,
            }
            return (
                self.report_template_id.report_action(self, data=data)
            )
