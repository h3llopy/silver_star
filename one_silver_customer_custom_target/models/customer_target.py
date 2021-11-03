from odoo import models, fields, api


class SalesOrderLines(models.Model):
    _inherit = "one.customer.target.line"

    @api.depends('product_template_id', 'product_id')
    @api.onchange('product_template_id', 'product_id')
    def _get_customer_products(self):
        customer_products = []
        if self.customer_id.allow_custom_product:
            customer_products = self.env['product.customerinfo'].search(
                [('name', '=', self.customer_id.id)]).mapped('product_tmpl_id')

            return {'domain': {
                'product_template_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_products.ids,
                'product_id': "[('id','in', %s),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" % customer_products.product_variant_ids.ids,
            }}


