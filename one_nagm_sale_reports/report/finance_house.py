""" Initialize Forward Sale """

from odoo import api, models


class FinanceHouseReport(models.AbstractModel):
    """
        Initialize Report One Silver Sale Report Finance House Template Id:
         -
    """
    _name = 'report.one_nagm_sale_reports.finance_house_template_id'
    _description = 'Finance House Report'

    def get_report_data(self, order_id=False):
        """ Get Report Data """

        order_id = self.env['sale.order'].search(
            [('id', '=', order_id)])
        return {
            'docs': order_id,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(
            self.get_report_data(data['order_id']))
        return data


class FinanceHouseInvoiceReport(models.AbstractModel):
    """
        Initialize Report One Silver Invoice  Finance House Template Id:
         -
    """
    _name = 'report.one_nagm_sale_reports.finance_inv_template_id'
    _description = 'Finance House Report'

    def get_report_data(self, inv_id=False):
        """ Get Report Data """

        inv_id = self.env['account.move'].search(
            [('id', '=', inv_id)])
        return {
            'docs': inv_id,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(
            self.get_report_data(data['inv_id']))
        return data
