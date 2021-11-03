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


    @api.depends('product_customer', 'main_sale_order', 'order_id.free_types')
    @api.onchange('product_customer', 'main_sale_order', 'order_id.free_types')
    def _get_customer_products(self):
        customer_products = []
        if self.order_id.partner_id.allow_custom_product:
            customer_products = self.env['product.customerinfo'].search([('name', '=', self.order_id.partner_id.id)]).mapped('product_tmpl_id').ids
            if self.order_id.based_sale_order or self.order_id.is_free_order or self.order_id.apply_free:
                free_types_global = self.env['one.free.type'].search([('customers_count','=',0),('id','in',self.order_id.free_types.ids)])
                free_types_global_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', free_types_global.ids+self.order_id.free_types.ids)])

                customer_free_standalone_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', self.order_id.free_types.ids),
                     ('id', '=', customer_products+free_types_global_products.ids)])
                return {'domain': {
                    'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.ids,
                    'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.product_variant_ids.ids,
                }}

        elif not self.order_id.partner_id.allow_custom_product:
            if self.order_id.based_sale_order or self.order_id.is_free_order or self.order_id.apply_free:
                free_types_global = self.env['one.free.type'].search([('customers_count','=',0),('id','in',self.order_id.free_types.ids)])
                free_types_global_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', free_types_global.ids+self.order_id.free_types.ids)])

                customer_free_standalone_products = self.env['product.template'].search(
                    [('allow_free', '=', True), ('free_types_allowed', 'in', self.order_id.free_types.ids)('id', '=', free_types_global_products.ids)])
                return {'domain': {
                    'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.ids,
                    'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_free_standalone_products.product_variant_ids.ids,
                }}


        else:
            return {'domain':
                {
                    'product_template_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                    'product_id': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                }
            }


