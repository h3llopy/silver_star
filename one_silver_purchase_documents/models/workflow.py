# -*- coding: utf-8 -*-
from odoo import fields, models


class WorkflowActionRulePurchase(models.Model):
    _inherit = ['documents.workflow.rule']

    has_business_option = fields.Boolean(default=True, compute='_get_business')
    create_model = fields.Selection(
        selection_add=[('purchase.order', "Purchase Order")])

    def create_record(self, documents=None):
        rv = super(WorkflowActionRulePurchase, self).create_record(
            documents=documents)
        if self.create_model == 'purchase.order':
            purchase = self.env[self.create_model].create({'partner_id': 1})
            image_is_set = False

            for document in documents:
                # this_document is the document in use for the workflow
                this_document = document
                if (
                        document.res_model or document.res_id) and document.res_model != 'documents.document':
                    attachment_copy = document.attachment_id.with_context(
                        no_document=True).copy()
                    this_document = document.copy(
                        {'attachment_id': attachment_copy.id})
                this_document.write({
                    'res_model': purchase._name,
                    'res_id': purchase.id,
                })
                if 'image' in this_document.mimetype and not image_is_set:
                    if this_document.partner_id:
                        purchase.write({'image_1920': this_document.datas,
                                        'partner_id': this_document.partner_id.id})
                    else:
                        purchase.write({'image_1920': this_document.datas})
                    image_is_set = True

            view_id = purchase.get_formview_id()
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'name': "New Purchase Order",
                'context': self._context,
                'view_mode': 'form',
                'views': [(view_id, "form")],
                'res_id': purchase.id if purchase else False,
                'view_id': view_id,
            }
        return rv
