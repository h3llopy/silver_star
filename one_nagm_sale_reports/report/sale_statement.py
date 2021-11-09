""" Initialize Customer Sales Statement """

from odoo import api, models


class  KuwaitFinanceHouse(models.AbstractModel):
    """
        Initialize Report One Nagm Sale Reports Kuwait Finance House:
         -
    """
    _name = 'report.one_nagm_sale_reports.kuwait_finance_house_id'
    _description = 'Report One Nagm Sale Reports Kuwait Finance House'

    def get_report_data(self, date_from=False, date_to=False,
                        partner_ids=False):
        """ Get Report Data """
        domain = []
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        if partner_ids:
            domain.append(('partner_id', 'in', partner_ids))
        order_ids = self.env['sale.report'].search(domain, order='partner_id')

        return {
            'date_from': date_from,
            'date_to': date_to,
            'order_ids': order_ids,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(
            self.get_report_data(data['date_from'], data['date_to'],
                                 data['partner_ids']))
        return data

class  KuwaitBankTemplate(models.AbstractModel):
    """
        Initialize Report One Nagm Sale Reports Kuwait Bank Template:
         -
    """
    _name = 'report.one_nagm_sale_reports.kuwait_bank_template_id'
    _description = 'Report One Nagm Sale Reports Kuwait Bank Template'

    def get_report_data(self, date_from=False, date_to=False):
        """ Get Report Data """
        domain = []
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        order_ids = self.env['sale.report'].search(domain, order='order_id')

        return {
            'date_from': date_from,
            'date_to': date_to,
            'order_ids': order_ids,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(
            self.get_report_data(data['date_from'], data['date_to']))
        return data

