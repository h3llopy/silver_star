""" Initialize Res Partner """

from odoo import fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    sale_report_id = fields.Many2one(
        'ir.actions.report', string="Sale Report Template",
        domain=[('model', '=', 'sale.select.report'),
                ('binding_model_id', '=', False)]
    )
    inv_report_id = fields.Many2one(
        'ir.actions.report', string="Inv Report Template",
        domain=[('model', '=', 'invoice.select.report'),
                ('binding_model_id', '=', False)]
    )
    partner_commission = fields.Float()
