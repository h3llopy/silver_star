# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'documents.mixin']

    image_1920 = fields.Binary()

    def _get_document_tags(self):
        company = self.company_id or self.env.company
        return company.purchase_tags

    def _get_document_folder(self):
        company = self.company_id or self.env.company
        return company.purchase_folder

    def _check_create_documents(self):
        company = self.company_id or self.env.company
        return company.documents_purchase_settings and super()._check_create_documents()
