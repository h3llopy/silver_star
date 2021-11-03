# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_purchase_settings = fields.Boolean(
        related='company_id.documents_purchase_settings', readonly=False,
        string="purchase"
    )
    purchase_folder = fields.Many2one(
        'documents.folder', related='company_id.purchase_folder', readonly=False,
        string="Purchase default workspace"
    )
    purchase_tags = fields.Many2many(
        'documents.tag', 'purchase_tags_table', related='company_id.purchase_tags',
        readonly=False, string="Purchase Tags"
    )

    @api.onchange('purchase_folder')
    def on_purchase_folder_change(self):
        if self.purchase_folder != self.purchase_tags.mapped('folder_id'):
            self.purchase_tags = False
