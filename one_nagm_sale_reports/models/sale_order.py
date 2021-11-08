""" Initialize Sale Order """

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
