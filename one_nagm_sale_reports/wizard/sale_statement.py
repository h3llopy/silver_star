""" Initialize Customer Sales Statement """

from odoo import fields, models


class SaleStatement(models.TransientModel):
    """
        Initialize  Sales Statement:
         -
    """
    _name = 'sale.statement'
    _description = 'Sales Statement'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    partner_ids = fields.Many2many(
        'res.partner'
    )
    select_report = fields.Selection(
        [
            ('finance_house', 'Kuwait Finance House'),
            ('international_center', 'Kuwait International Bank')
        ],
        default='finance_house'
    )

    def print_report(self):
        """ Print Report """
        form = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_ids': self.partner_ids.ids,
        }
        if self.select_report == 'finance_house':
            return (
                self.env.ref(
                    'one_nagm_sale_reports.kuwait_finance_house_report').report_action(
                    self, data=form))
        else:
            return (
                self.env.ref(
                    'one_nagm_sale_reports.kuwait_bank_report').report_action(
                    self, data=form))
