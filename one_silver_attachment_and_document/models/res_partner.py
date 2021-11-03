""" Initialize Res Partner """

from odoo import fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    upload_documents = fields.Boolean()
    sale_document = fields.Boolean(string='Sale')
    purchase_document = fields.Boolean(string='Purchase')
