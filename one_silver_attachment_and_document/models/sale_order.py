""" Initialize Sale Order """

from odoo import api, fields, models


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         - 
    """
    _inherit = 'sale.order'

    document_id = fields.Many2one(
        'documents.document', copy=False,
        domain="[('sale_id', '=', False),('purchase_id', '=', False)]"
    )
    sale_document = fields.Boolean(
        related='partner_id.sale_document'
    )

    @api.model
    def create(self, vals_list):
        """ Override create """
        res = super(SaleOrder, self).create(vals_list)
        if 'document_id' in vals_list and vals_list['document_id']:
            res.document_id.write({'select_model': 'sale', 'sale_id': res.id})
            res.document_id._change_attachment_model('sale_order')
        return res

    def write(self, vals):
        """ Override write """
        old_document = self.document_id
        res = super(SaleOrder, self).write(vals)
        if 'document_id' in vals:
            if self.document_id:
                self.document_id.write(
                    {'select_model': 'sale', 'sale_id': self.id})
                self.document_id._change_attachment_model('sale_order')
                if old_document:
                    old_document.write(
                        {'select_model': False, 'sale_id': False})
                    old_document._change_attachment_model('document')
            else:
                if old_document:
                    old_document.write(
                        {'select_model': False, 'sale_id': False})
                    old_document._change_attachment_model('document')

        return res

    def unlink(self):
        """ Override unlink """
        self.document_id._change_attachment_model('document')
        return super(SaleOrder, self).unlink()
