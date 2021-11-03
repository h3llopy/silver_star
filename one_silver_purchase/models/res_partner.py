""" Initialize Res Partner """

from odoo import fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    shipping_type = fields.Selection(
        [('internal', 'Internal'), ('external', 'External')],
        default='internal'
    )
