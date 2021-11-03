""" Initialize Purchase Order """

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    """
        Inherit Purchase Order:
         -
    """
    _inherit = 'purchase.order'

    document_id = fields.Many2one(
        'documents.document', copy=False,
        domain="[('purchase_id', '=', False),('sale_id', '=', False)]"
    )
    purchase_document = fields.Boolean(
        related='partner_id.purchase_document'
    )

    @api.model
    def create(self, vals_list):
        """ Override create """
        res = super(PurchaseOrder, self).create(vals_list)
        if 'document_id' in vals_list and vals_list['document_id']:
            res.document_id.write(
                {'select_model': 'purchase', 'purchase_id': res.id})
            res.document_id._change_attachment_model('purchase_order')
        return res

    def write(self, vals):
        """ Override write """
        old_document = self.document_id
        res = super(PurchaseOrder, self).write(vals)

        if 'document_id' in vals:
            if self.document_id:
                self.document_id.write(
                    {'select_model': 'purchase', 'purchase_id': self.id})
                self.document_id._change_attachment_model('purchase_order')
                if old_document:
                    old_document.write(
                        {'select_model': False, 'purchase_id': False})
                    old_document._change_attachment_model('document')
            else:
                if old_document:
                    old_document.write(
                        {'select_model': False, 'purchase_id': False})
                    old_document._change_attachment_model('document')
        return res

    def unlink(self):
        """ Override unlink """
        self.document_id._change_attachment_model('document')
        return super(PurchaseOrder, self).unlink()
