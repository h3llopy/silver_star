#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / product.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields, api


class CustomerInfo(models.Model):
    _name = "product.customerinfo"
    _description = "Customer Pricelist"
    _order = 'sequence, min_qty desc, price'

    name = fields.Many2one(
        'res.partner', 'Customer',
        ondelete='cascade', required=True,
        help="Customer of this product", check_company=True)
    product_name = fields.Char(
        'Customer Product Name',
        help="This customer's product name will be used when printing a quotation. Keep empty to use the internal one.")
    product_code = fields.Char(
        'Customer Product Code',
        help="This customer's product code will be used when printing a  quotation. Keep empty to use the internal one.")
    barcode = fields.Char('Barcode',)

    sequence = fields.Integer(
        'Sequence', default=1, help="Assigns the priority to the list of product customer.")
    product_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        related='product_tmpl_id.uom_po_id',
        help="This comes from the product form.")
    min_qty = fields.Float(
        'Quantity', default=0.0, required=True, digits="Product Unit Of Measure",
        help="The quantity to sales to this customer to benefit from the price, expressed in the customer Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")
    price = fields.Float(
        'Price', default=0.0, digits='Product Price',
        required=True, help="The price to sales a product")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company.id, index=1)
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True)
    date_start = fields.Date('Start Date', help="Start date for this customer price")
    date_end = fields.Date('End Date', help="End date for this customer price")
    product_id = fields.Many2one(
        'product.product', 'Product Variant', check_company=True,
        help="If not set, the customer price will apply to all variants of this product.")
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', related='product_id.product_tmpl_id', string='Product Template', check_company=True,
        index=True, ondelete='cascade')
    product_variant_count = fields.Integer('Variant Count', related='product_tmpl_id.product_variant_count')
    delay = fields.Integer(
        'Delivery Lead Time', default=1, required=True,
        help="Lead time in days between the confirmation of the purchase order and the receipt of the products in your warehouse. Used by the scheduler for automatic computation of the purchase order planning.")
    is_allow_free_product = fields.Boolean(related='product_tmpl_id.allow_free')


    @api.onchange('is_allow_free_product')
    def _get_is_allow_free_product(self):
        if self.is_allow_free_product:
            return {'domain': {
                'name': "[('allow_custom_product', '=', True  ), ('allow_free_product', '=', True)]"}}
        else:
            return {'domain':
                {
                    'name': "[('allow_custom_product', '=', True  ), ('allow_free_product', '=', False)]"}
            }



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    allow_customer = fields.Boolean(string='Allow Customer', default=False)
    customers_ids = fields.One2many('product.customerinfo', 'product_id', 'Customers',
                                    help="Define customer pricelists.")
    variant_customers_ids = fields.One2many('product.supplierinfo', 'product_id')

    customer_price = fields.Integer(compute='get_product_customer_price')
    from_customer = fields.Boolean(compute='get_product_customer_price', store=False)
    customer_product_count = fields.Integer(compute='get_customer_product_count')

    #
    def get_product_customer_price(self):
        from_customer_inet = self._context['from_customer'] if 'from_customer' in self._context else False
        for record in self:
            record.from_customer = from_customer_inet
            if from_customer_inet:
                customer_product = self.env['product.customerinfo'].search(
                    [('name', '=', self._context['active_id']), ('product_id', '=', record.id)])
                record.customer_price = customer_product.price
            else:
                record.customer_price = 0.0

    def get_customer_product_count(self):
        self.customer_product_count = self.env['product.customerinfo'].search_count([('product_tmpl_id', '=', self.id)])

    def get_customer_product(self):
        self.ensure_one()
        customer_products = self.env['product.customerinfo'].search([('product_tmpl_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'view_mode': 'tree',
            'res_model': 'product.customerinfo',
            'domain': [('id', 'in', customer_products.ids)],
            'context': "{'create': False,}"
        }

    def action_add_customer_show_wizard(self):

        return {'type': 'ir.actions.act_window',
                'name': 'Add Customer',
                'res_model': 'one.customer.custom.product.add.wizard',
                'target': 'new',
                'view_id': self.env.ref('one_silver_custom_product.one_customer_custom_product_add_wizard_form_view').id,
                'view_mode': 'form',
                'context': {'product_tmpl_id': self.id}
                }


    # search by customer product name and code
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if 'partner' in self._context:
            products = self.env['product.customerinfo'].search([('name', 'ilike', args)]).mapped('product_id')
            if products:
                return products

        return super(ProductTemplate, self).name_search(name, args=args, operator=operator, limit=limit)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    customer_product_count = fields.Integer(compute='get_customer_product_count')

    def get_customer_product_count(self):
        self.customer_product_count = self.env['product.customerinfo'].search_count([('product_id', '=', self.id)])

    def action_add_customer_show_wizard(self):

        return {'type': 'ir.actions.act_window',
                'name': 'Add Customer',
                'res_model': 'one.customer.custom.product.add.wizard',
                'target': 'new',
                'view_id': self.env.ref(
                    'one_silver_custom_product.one_customer_custom_product_add_wizard_form_view').id,
                'view_mode': 'form',
                'context': {'product_id': self.id}
                }

    # search by customer product name and code
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if 'partner' in self._context:
            products = self.env['product.customerinfo'].search([('name', 'ilike', args)]).mapped('product_id')
            if products:
                return products

        return super(ProductProduct, self).name_search(name, args=args, operator=operator, limit=limit)


class CustomerCustomProductAddWizard(models.Model):
    _name = 'one.customer.custom.product.add.wizard'

    @api.depends('customer_ids')
    @api.onchange('customer_ids')
    def _get_customers_domain(self):
        product_tmpl_id = False
        product_id = False
        if self._context['active_model'] == 'product.template':
            product_tmpl_id = self.env['product.template'].search([('id', '=', self._context['active_id'])])
            product_id = self.env['product.product'].search([('id', '=', product_tmpl_id.product_variant_id.id)])
        if self._context['active_model'] == 'product.product':
            product_id = self.env['product.product'].search([('id', '=', self._context['active_id'])])
            product_tmpl_id = self.env['product.template'].search([('id', '=', product_id.product_tmpl_id.id)])
        list_ids = []
        if product_id and product_tmpl_id:
            customers_in_products_tmpl = self.env['product.customerinfo'].search(
                [('product_id', '=', product_id.id), ('product_tmpl_id', '=', product_tmpl_id.id)]).mapped('name').ids
            for custip in customers_in_products_tmpl:
                list_ids.append(custip)
        customers_parners_allow_product = self.env['res.partner'].search([('allow_custom_product', '=', False)]).ids

        for custpap in customers_parners_allow_product:
            list_ids.append(custpap)
        return {'domain': {'customer_ids': "[('id','not in', %s)]" % list_ids}}

    customer_ids = fields.Many2many(comodel_name='res.partner', string='Customers',
                                    relation='customer_custom_product_add_rel', )

    def action_save(self):
        product_tmpl_id = False
        product_id = False
        if self.customer_ids:
            if self._context['active_model'] == 'product.template':
                product_tmpl_id = self.env['product.template'].search([('id', '=', self._context['active_id'])])
                product_id = self.env['product.product'].search([('id', '=', product_tmpl_id.product_variant_id.id)])
            if self._context['active_model'] == 'product.product':
                product_id = self.env['product.product'].search([('id', '=', self._context['active_id'])])
                product_tmpl_id = self.env['product.template'].search([('id', '=', product_id.product_tmpl_id.id)])

            for customer in self.customer_ids:
                self.env['product.customerinfo'].create({
                    'name': customer.id,
                    'company_id': self.env.company.id,
                    'product_tmpl_id': product_tmpl_id.id,
                    'product_id': product_id.id,
                })

class SaleOrderFreeProduct(models.Model):
    _inherit = "one.sale.order.free.product"

    @api.depends('product_id', 'product_tmpl_id')
    @api.onchange('product_id', 'product_tmpl_id')
    def get_per_free_products(self):
        list_ids = []
        per_free_products = self.env['one.sale.order.free.product'].search([('sale_order_id', '=', self.sale_order_id.id)])

        customer_allowed_products = self.env['product.customerinfo'].search([('name', '=', self.sale_order_id.partner_id.id)])
        if self.sale_order_id.partner_id.allow_custom_product:
            return {'domain': {

                'product_id': [('product_tmpl_id', '=', self.product_tmpl_id.id),
                               ('id', 'in', customer_allowed_products.mapped('product_id').ids),
                               ('id', 'not in', per_free_products.mapped('product_id').ids), ('allow_free', '=', True)],

                'product_tmpl_id': [
                    ('id', 'in', customer_allowed_products.mapped('product_tmpl_id').ids),
                    ('id', 'not in', per_free_products.mapped('product_tmpl_id').ids), ('allow_free', '=', True)],
            }}
        if not self.sale_order_id.partner_id.allow_custom_product:
            return {'domain': {

                'product_id': [('product_tmpl_id', '=', self.product_tmpl_id.id),
                               ('id', 'not in', per_free_products.mapped('product_id').ids), ('allow_free', '=', True)],

                'product_tmpl_id': [('id', 'not in', per_free_products.mapped('product_tmpl_id').ids), ('allow_free', '=', True)], }}
