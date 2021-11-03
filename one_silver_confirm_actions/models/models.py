# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderInheritConfirm(models.Model):
    _inherit = "sale.order"

    def confirm_order_server_action(self):
        for rec in self:
            if rec.state in ['draft', 'sent']:
                rec.action_confirm()

    def create_order_server_action(self):
        for rec in self:
            delivered = True
            for line in rec.order_line:
                if line.product_uom_qty != line.qty_delivered:
                    delivered = False
            if delivered:
                rec._create_invoices()
            else:
                raise UserError(_('The Sale Order is Not Delivered.'))

class PurchaseOrderInheritConfirm(models.Model):
    _inherit = "purchase.order"

    def confirm_purchase_order_server_action(self):
        for rec in self:
            if rec.state in ['draft', 'sent']:
                rec.button_confirm()

    def create_order_server_action(self):
        for rec in self:
            delivered = True
            for line in rec.order_line:
                if line.product_qty != line.qty_received:
                    delivered = False
            if delivered:
                rec.action_create_invoice()
            else:
                raise UserError(_('The Purchase Order is Not Delivered.'))