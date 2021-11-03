""" Initialize Document """

from odoo import api, fields, models


class DocumentsDocument(models.Model):
    """
        Inherit Documents Document:
         -
    """
    _inherit = 'documents.document'

    select_model = fields.Selection(
        [('sale', 'Sale'),
         ('purchase', 'Purchase')],
    )
    sale_id = fields.Many2one(
        'sale.order', string='SO'
    )
    purchase_id = fields.Many2one(
        'purchase.order', string='PO'
    )

    @api.onchange('select_model')
    def _onchange_select_model(self):
        """ onchange  select_model """
        if self.select_model == 'sale':
            self.purchase_id = False
        else:
            self.sale_id = False

    @api.model
    def create(self, vals):
        keys = [key for key in vals if
                self._fields[key].related and self._fields[key].related[
                    0] == 'attachment_id']
        attachment_dict = {key: vals.pop(key) for key in keys if key in vals}
        attachment = self.env['ir.attachment'].browse(vals.get('attachment_id'))

        if attachment and attachment_dict:
            attachment.write(attachment_dict)
        elif attachment_dict:
            attachment_dict.setdefault('name', vals.get('name', 'unnamed'))
            attachment = self.env['ir.attachment'].create(attachment_dict)
            vals['attachment_id'] = attachment.id
        new_record = super(DocumentsDocument, self).create(vals)

        # this condition takes precedence during forward-port.
        if (attachment and not attachment.res_id and (
                not attachment.res_model or attachment.res_model == 'documents.document')):
            if new_record.select_model == 'sale':
                attachment.with_context(no_document=True).write(
                    {'res_model': 'sale.order',
                     'res_id': new_record.sale_id.id,
                     })
            elif new_record.select_model == 'purchase':
                attachment.with_context(no_document=True).write(
                    {'res_model': 'purchase.order',
                     'res_id': new_record.purchase_id.id,
                     })
            else:
                attachment.with_context(no_document=True).write(
                    {'res_model': 'documents.document',
                     'res_id': new_record.id})
        else:
            if new_record.select_model == 'sale':
                attachment.with_context(no_document=True).write(
                    {'res_model': 'sale.order',
                     'res_id': new_record.sale_id.id,
                     })
            elif new_record.select_model == 'purchase':
                attachment.with_context(no_document=True).write(
                    {'res_model': 'purchase.order',
                     'res_id': new_record.purchase_id.id,
                     })
        return new_record

    def _change_attachment_model(self, model_name):
        """ Change Document """
        if model_name == 'sale_order':
            self.attachment_id.with_context(no_document=True).write(
                {'res_model': 'sale.order',
                 'res_id': self.sale_id.id})
        elif model_name == 'purchase_order':
            self.attachment_id.with_context(no_document=True).write(
                {'res_model': 'purchase.order',
                 'res_id': self.purchase_id.id})
        else:
            self.attachment_id.with_context(no_document=True).write(
                {'res_model': 'documents.document',
                 'res_id': self.id})

    def write(self, vals):
        """ Override write """
        res = super(DocumentsDocument, self).write(vals)
        if 'sale_id' in vals and self.sale_id and self.select_model == 'sale':
            self._change_attachment_model('sale_order')
        elif 'purchase_id' in vals and self.purchase_id and self.select_model == 'purchase':
            self._change_attachment_model('purchase_order')
        else:
            self._change_attachment_model('document')
        return res
