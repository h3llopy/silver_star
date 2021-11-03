#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / sales_order.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields, api


class SalesOrderLines(models.Model):
    _inherit = "sale.order.line"

    # domain for just products that assigned for customer brfore
    product_customer = fields.Many2one('res.partner', related='order_id.partner_id')


    @api.depends('product_customer', 'main_sale_order')
    @api.onchange('product_customer', 'main_sale_order')
    def _get_customer_products(self):
        customer_products = []
        if self.order_id.partner_id.allow_custom_product:
            customer_products = self.env['product.customerinfo'].search(
                [('name', '=', self.order_id.partner_id.id)]).mapped('product_tmpl_id').ids

            if self.order_id.based_sale_order or self.order_id.is_free_order:
                customer_free_standalone_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', self.order_id.free_types.ids),
                     ('id', '=', customer_products)])
                return {'domain': {
                    'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.ids,
                    'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.product_variant_ids.ids,
                }}

        elif not self.order_id.partner_id.allow_custom_product:
            if self.order_id.based_sale_order or self.order_id.is_free_order:
                customer_free_standalone_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', self.order_id.free_types.ids)])
                return {'domain': {
                    'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.ids,
                    'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.product_variant_ids.ids,
                }}

        if self.order_id.partner_id.allow_custom_product:
            customer_products = self.env['product.customerinfo'].search(
                [('name', '=', self.order_id.partner_id.id)]).mapped('product_tmpl_id')
            return {'domain': {
                'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_products.ids,
                'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_products.product_variant_ids.ids,

            }}

        if not self.order_id.partner_id.allow_custom_product:
            return {'domain': {
                'product_template_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                'product_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]"

            }}
        else:
            return {'domain':
                {
                    'product_template_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                    'product_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                }
            }
