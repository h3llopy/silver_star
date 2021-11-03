# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'documents.mixin']

    image_1920 = fields.Binary()

    def _get_document_tags(self):
        company = self.company_id or self.env.company
        return company.sale_tags

    def _get_document_folder(self):
        company = self.company_id or self.env.company
        return company.sale_folder

    def _check_create_documents(self):
        company = self.company_id or self.env.company
        return company.documents_sale_settings and super()._check_create_documents()
