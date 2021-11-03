#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / free_types.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import fields, models, api, _
from odoo.osv import expression


class FreeType(models.Model):
    _name = 'one.free.type'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    percentage = fields.Float(string="Percentage", default=0.0, required=True)
    amount = fields.Float(string="Amount", default=0.0, required=True)
    company_id = fields.Many2one('res.company', string='Company')
    color = fields.Integer("Color Index", default=0)
    active = fields.Boolean(string="Active", default=True)
    not_percent = fields.Boolean(string="No Percent", default=False)
    type_type = fields.Selection(selection=[('standalone', 'Standalone'), ('embedded', 'Embedded')],
                                 string='Sale Order Insert', default='embedded', required=True)

    customers_ids = fields.Many2many(comodel_name='one.free.type.customer', string='Customers', inverse_name='free_type_id', select=True)
    customers_count = fields.Integer(compute='compute_customer_count')
    products_count = fields.Integer(compute='compute_product_count')

    def action_add_customers_wizard(self):
        customers_ids = self.env['one.free.type.customer'].search([('free_type_id', '=', self.id)]).customer_id.ids
        return {'type': 'ir.actions.act_window',
                'name': _('Add Customer'),
                'res_model': 'one.free.type.customer.wizard',
                'target': 'new',
                'view_id': self.env.ref('one_silver_free_products.add_customers_wizard').id,
                'view_mode': 'form',
                'context': {'default_free_type': self.id}
                }

    def get_customers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customers',
            'view_mode': 'tree',
            'res_model': 'one.free.type.customer',
            'context': {'create': False, },
            'domain': [('free_type_id', '=', self.id)]
        }

    def compute_customer_count(self):
        for record in self:
            record.customers_count = self.env['one.free.type.customer'].search_count(
                [('free_type_id', '=', self.id)])

    def get_products(self):
        view = self.env.ref('one_silver_free_products.product_product_tree_view')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'view_mode': 'tree',
            'res_model': 'product.product',
            'view_id': view.id,
            'context': {
                'edit': False,
                'create': False,
                'delete': False,
                'duplicate': False,
            },
            'domain': [('free_types_allowed', 'in', self.id)]
        }

    def compute_product_count(self):
        for record in self:
            record.products_count = self.env['product.product'].search_count([('free_types_allowed', 'in', record.id)])

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = [('id', 'in', [])]
        if 'sale_order' in self.env.context:
            sale_order = self.env['sale.order'].search([('id', '=', self.env.context.get('sale_order'))])
            if sale_order.partner_id:
                frees_ids = []
                if sale_order.is_free_order and not sale_order.based_sale_order:
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', sale_order.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                         ('free_type_id.not_percent', '=', True)]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    res = [('id', 'in', frees_ids)]
                if not sale_order.is_free_order and not sale_order.based_sale_order:
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', sale_order.partner_id.id), ('free_type_id.type_type', '=', 'embedded')]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    res = [('id', 'in', frees_ids)]
                if not sale_order.is_free_order and sale_order.based_sale_order:
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', sale_order.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                         ('free_type_id.not_percent', '=', False)]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    res = [('id', 'in', frees_ids)]

            return super().search_read(domain=res, fields=fields, offset=offset, limit=limit, order=order)
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if 'customer_id' in self.env.context and self.env.context.get('customer_id'):
            frees = [('id', 'in', [])]
            if self.env.context.get('customer_id'):
                frees_ids = []
                if self.env.context.get('is_free_order') and not self.env.context.get('based_sale_order'):
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', self.env.context.get('customer_id')), ('free_type_id.type_type', '=', 'standalone'),
                         ('free_type_id.not_percent', '=', True)]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    frees = [('id', 'in', frees_ids)]
                if not self.env.context.get('is_free_order') and not self.env.context.get('based_sale_order'):
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', self.env.context.get('customer_id')), ('free_type_id.type_type', '=', 'embedded')]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    frees = [('id', 'in', frees_ids)]
                if not self.env.context.get('is_free_order') and self.env.context.get('based_sale_order'):
                    customer_frees = self.env['one.free.type.customer'].search(
                        [('customer_id', '=', self.env.context.get('customer_id')), ('free_type_id.type_type', '=', 'standalone'),
                         ('free_type_id.not_percent', '=', False)]).free_type_id.ids
                    global_frees = self.env['one.free.type'].search(
                        [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids)]).ids
                    for x in customer_frees:
                        frees_ids.append(x)
                    for y in global_frees:
                        frees_ids.append(y)
                    frees = [('id', 'in', frees_ids)]
            return super(FreeType, self).name_search(name, args=expression.AND([frees, args]), operator=operator, limit=limit)
        else:
            return super(FreeType, self).name_search(name, args=args, operator=operator, limit=limit)


class FreeTypeCustomers(models.Model):
    _name = 'one.free.type.customer'
    free_type_id = fields.Many2one(comodel_name='one.free.type', string='Free Type')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', domain=[('allow_free_product', '=', True)])
    free_amount = fields.Float(string="Amount", required=True, readonly=False)
    free_percent = fields.Float(string="Percentage", required=True, readonly=False)

    @api.onchange('free_type_id')
    def _onchange_free_type_id(self):
        self.free_amount = self.free_type_id.amount
        self.free_percent = self.free_type_id.percentage


class FreeTypeCustomerWizard(models.TransientModel):
    _name = 'one.free.type.customer.wizard'
    free_type = fields.Many2one(comodel_name='one.free.type', )

    @api.depends('customers_ids')
    @api.onchange('customers_ids')
    def get_dom(self):
        customers_ids = self.env['one.free.type.customer'].search([('free_type_id', '=', self.env.context['default_free_type'])]).customer_id.ids
        return {'domain': {'customers_ids': [('allow_free_product', '=', True), ('id', 'not in', customers_ids)]}}

    customers_ids = fields.Many2many(comodel_name='res.partner', string='Customers')

    def save_customers(self):
        for record in self.customers_ids:
            free_type = self.env['one.free.type'].search([('id', '=', self.env.context['active_id'])])
            self.env['one.free.type.customer'].create({
                'free_type_id': free_type.id,
                'customer_id': record.id,
                'free_amount': free_type.amount,
                'free_percent': free_type.percentage
            })
