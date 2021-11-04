#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / sale_order.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_free_order = fields.Boolean(string='Is free Order', default=False)
    is_customer_allow_free = fields.Boolean(related='partner_id.allow_free_product')

    apply_free = fields.Boolean(string='Apply Free Products')

    free_types = fields.Many2many(comodel_name='one.free.type', string='Applied Free Types',
                                  relation='sale_order_free_types_rel')
    free_method = fields.Selection(selection=[('percent', 'Percentage'), ('amount', 'Amount')], default='percent')
    free_total = fields.Monetary(string='Free Total')
    sales_order_add_free_products = fields.One2many(comodel_name='one.sale.order.free.product', string='Products',
                                                    inverse_name='sale_order_id')
    amount_total_with_free = fields.Float(string='Final', store=True)

    def get_used_free_amount(self):
        total = 0.0
        for record in self.sales_order_add_free_products:
            total += record.unit_total
        self.amount_free_used = total
        self.amount_free_remin = (self.free_total - self.amount_free_used - self.related_free_sales_order_total)

    amount_free_used = fields.Float(string='Free Used', store=False, compute=get_used_free_amount)
    amount_free_remin = fields.Float(string='Free Remin', store=False, compute=get_used_free_amount)
    based_sale_order = fields.Boolean(default=False)
    main_sale_order = fields.Many2one(comodel_name='sale.order', string='Main Sale Order', store=True)
    free_remin_main_sale_order = fields.Float(related='main_sale_order.amount_free_remin')
    related_sale_orders = fields.One2many(comodel_name='sale.order', string='Related Sales Orders',
                                          inverse_name='main_sale_order',
                                          domain=[('based_sale_order', '=', True)])
    free_total_inner_free_order = fields.Float(string='Free Total', store=True, compute='_calc_free_order_free')
    reload_lines = fields.Boolean(store=False, )
    related_free_sales_order_total = fields.Float(string='Related Sale Order Free',
                                                  compute='_get_related_free_sale_order_total')
    open_dialog=fields.Boolean(store=False)



    def name_get(self):
        if self.partner_id:
            frees_ids = []
            if self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', True)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            elif not self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'embedded')]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'embedded')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            elif not self.is_free_order and self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', False)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone'),
                     ('not_percent', '=', False)]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            return {'domain': {'free_types': frees}}

    @api.depends('free_types')
    @api.onchange('free_types')
    def _domain_free_types(self):
        if self.partner_id:
            frees_ids = []
            if self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', True)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            elif not self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'embedded')]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'embedded')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            elif not self.is_free_order and self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', False)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone'),
                     ('not_percent', '=', False)]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            return {'domain': {'free_types': frees}}
        # return super(SaleOrder, self).name_get()

    @api.onchange('order_line', 'amount_total', 'free_method', 'free_types')
    @api.depends('order_line', 'amount_total', 'free_method', 'free_types')
    @api.constrains('amount_total')
    def _calculate_free_total(self):
        for record in self:
            if not record.based_sale_order:
                if record.order_line:
                    if record.apply_free:
                        record.free_total = 0.0
                        if record.free_method == 'percent':
                            if record.free_types:
                                main_percent = 0.0
                                for free in record.free_types:
                                    customer_percent = free.percentage
                                    customer_obj = free.customers_ids.search(
                                        [('free_type_id', '=', free.ids), ('customer_id', '=', record.partner_id.id)])
                                    if customer_obj:
                                        customer_percent = customer_obj.free_percent
                                    main_percent += customer_percent
                                record.free_total = ((record.amount_total * main_percent) / 100)
                        elif record.free_method == 'amount':
                            if record.free_types:
                                main_total = 0.0
                                for free in record.free_types:
                                    customer_amount = free.amount
                                    customer_obj = free.customers_ids.search(
                                        [('free_type_id', '=', free.ids), ('customer_id', '=', record.partner_id.id)])
                                    if customer_obj:
                                        customer_amount = customer_obj.free_amount
                                    main_total += customer_amount
                                if main_total >= record.amount_total:
                                    raise ValidationError('total free amount is > invoice total')
                                else:
                                    record.free_total = main_total

                        record.amount_total_with_free = record.amount_total + record.free_total
                    else:
                        record.free_total = 0.0
                else:
                    record.free_total = 0.0
            else:
                record.free_total = 0.0
        total = 0.0
        for record in self.sales_order_add_free_products:
            total += record.unit_total
        self.amount_free_used = total
        self.amount_free_remin = (self.free_total - self.amount_free_used - self.related_free_sales_order_total)

    def action_add_free_product_wizard(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Add Free Products'),
                'res_model': 'one.sale.order.free.product.add.wizard',
                'target': 'new',
                'view_id': self.env.ref('one_silver_free_products.sale_order_add_free_product_wizard').id,
                'view_mode': 'form',
                'context': {'default_sale_order_id': self.id,
                            'default_free_type_type': 'embedded' if not self.based_sale_order else 'standalone'}
                }

    def new_sale_order_create(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Free Inner Sale Order'),
            'res_model': 'sale.order',
            'target': 'current',
            'view_id': self.env.ref(
                'one_silver_free_products.sale_order_form_view_inherit').id,
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.partner_id.id,
                # 'default_industry_id': self.industry_id.id,
                'default_based_sale_order': True,
                'default_apply_free': True,
                'default_free_method': self.free_method,
                'default_main_sale_order': self.id,
                'default_pricelist_id': self.pricelist_id.id,
                'default_free_types': [(6, 0, [])],
            }
        }

    @api.depends('related_sale_orders')
    @api.onchange('related_sale_orders')
    def _get_related_free_sale_order_total(self):
        for record in self:
            record.related_free_sales_order_total = sum(
                [(sol.free_total_inner_free_order) for sol in record.related_sale_orders])

    @api.onchange('based_sale_order')
    def _onchange_selfbased_sale_order(self):
        if self.based_sale_order:
            self.apply_free = True
        else:
            self.apply_free = False

    @api.onchange('is_free_order')
    def _onchange_is_free_order(self):
        lines_removed = []
        if self.is_free_order:
            self.apply_free = True
        else:
            self.apply_free = True
        if self.is_free_order and not self.based_sale_order:
            self.free_method = 'percent'
            self.free_types = [(6, 0, [])]
            self.free_types = self.env['one.free.type'].search(
                [('type_type', '=', 'standalone'), ('not_percent', '=', True), (
                    'id', 'in',
                    self.env['res.partner'].search([('id', '=', self.partner_id.id)]).free_types_allowed.ids)])

            self.order_line = [(6, 0, [])]
            return {
                'domain': {
                    'free_types': [('type_type', '=', 'standalone'), ('not_percent', '=', True)],
                    'partner_id': [('allow_free_product', '=', True)],
                }
            }
        if not self.is_free_order and not self.based_sale_order:
            self.free_types = [(6, 0, [])]
            self.free_types = self.env['one.free.type'].search(
                [('type_type', '=', 'embedded'), (
                    'id', 'in',
                    self.env['res.partner'].search([('id', '=', self.partner_id.id)]).free_types_allowed.ids)])
            self.order_line = [(6, 0, [])]

            return {'domain': {'free_types': [('type_type', '=', 'embedded')],
                               'partner_id': ['|', ('allow_free_product', '=', False), ('allow_free_product', '=', True)], }}
        if not self.is_free_order and self.based_sale_order:
            self.free_types = [(6, 0, [])]
            self.order_line = [(6, 0, [])]

            return {'domain': {'free_types': [('type_type', '=', 'standalone'), ('not_percent', '=', False)]}}

    @api.depends('order_line')
    @api.onchange('order_line')
    def _check_total_standalone_free(self):
        if self.based_sale_order:
            free_total = 0.0
            for line in self.order_line:
                line.price_unit = 0.0
                free_total += (line.origin_price_unit * line.product_uom_qty)
                if free_total > self.main_sale_order.amount_free_remin:
                    raise ValidationError('You exceed remaining free total in main sale order')

    @api.depends('order_line')
    @api.onchange('order_line')
    def _calc_free_order_free(self):
        for record in self:
            free_total = 0.0
            if record.based_sale_order:
                for line in record.order_line:
                    line.price_unit = 0.0
                    free_total += (line.origin_price_unit * line.product_uom_qty)
            if record.is_free_order:
                for line in record.order_line:
                    line.discount = 100
            record.free_total_inner_free_order = free_total

    @api.onchange('order_line')
    def changed_lines(self):
        lines_changed_ids = []
        for i in self.order_line:
            if i.reload_lines:
                lines_changed_ids.append(i)
        if lines_changed_ids:
            self.reload_lines = True
        else:
            self.reload_lines = False

    @api.onchange('reload_lines')
    def changed_reload_lines(self):
        if self.reload_lines:
            return {'value': {'order_line': [(2, val.id) for val in self.order_line if val.is_free]}}
        else:
            pass

    @api.depends('pricelist_id', 'user_limit_method', 'free_method', 'free_types')
    @api.onchange('pricelist_id', 'user_limit_method', 'free_method', 'free_types')
    def _onchange_pricelist_id(self):
        self.env['sale.order.line'].search([('order_id', 'in', self.ids), ('is_free', '=', True)]).unlink()
        self.env['one.sale.order.free.product'].search([('sale_order_id', 'in', self.ids)]).unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.depends('partner_id', )
    @api.onchange('partner_id', )
    def _onchage_partner_id(self):
        self.free_types = [(6, 0, [])]
        if self.partner_id:
            frees_ids = []
            if self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', True)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            if not self.is_free_order and not self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'embedded')]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'embedded')]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            if not self.is_free_order and self.based_sale_order:
                customer_frees = self.env['one.free.type.customer'].search(
                    [('customer_id', '=', self.partner_id.id), ('free_type_id.type_type', '=', 'standalone'),
                     ('free_type_id.not_percent', '=', False)]).free_type_id.ids
                global_frees = self.env['one.free.type'].search(
                    [('id', 'not in', self.env['one.free.type.customer'].search([]).free_type_id.ids), ('type_type', '=', 'standalone'),
                     ('not_percent', '=', False)]).ids
                for x in customer_frees:
                    frees_ids.append(x)
                for y in global_frees:
                    frees_ids.append(y)
                frees = [('id', 'in', frees_ids)]
            return {'domain': {'free_types': frees}}

    @api.model
    def create(self, vals_list):
        if not vals_list['order_line']:
            raise ValidationError('Can\'t save order without lines')
        else:
            return super(SaleOrder, self).create(vals_list)


class SalesOrderLines(models.Model):
    _inherit = "sale.order.line"

    is_free = fields.Boolean(string='Is Free', default=False)
    main_sale_order = fields.Many2one(comodel_name='sale.order', related='order_id.main_sale_order')
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', related='order_id.pricelist_id')
    based_sale_order = fields.Boolean(related='order_id.based_sale_order')
    apply_free = fields.Boolean(related='order_id.apply_free')
    is_free_order = fields.Boolean(related='order_id.is_free_order')
    reload_lines = fields.Boolean(store=False, )

    @api.depends('product_uom_qty', 'price_unit', 'discount', )
    @api.onchange('product_uom_qty', 'price_unit', 'discount', )
    def onchange_qty_unit_price_id(self):
        self.reload_lines = True

    def unlink(self):
        for record in self:
            self.env['one.sale.order.free.product'].search(
                [('sale_order_id', '=', record.order_id.id), ('sale_order_line', '=', record.id)]).unlink()
        return super(SalesOrderLines, self).unlink()


class SaleOrderFreeProduct(models.Model):
    _name = 'one.sale.order.free.product'
    _rec_name = 'product_id'

    company_id = fields.Many2one(related='sale_order_id.company_id', string='Company', store=True, readonly=True,
                                 index=True)

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sales Order')

    @api.depends('product_tmpl_id', 'product_id')
    @api.onchange('product_tmpl_id', 'product_id')
    def _product_tmpl_domain_product(self):
        return {
            'domain': {
                'product_id': [('product_tmpl_id', '=', self.product_tmpl_id.id), ('allow_free', '=', True)]
            }
        }

    product_id = fields.Many2one(
        'product.product', string='Product Variant',
        change_default=True, ondelete='restrict', check_company=True, readonly=False, )  # Unrequired company
    product_tmpl_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id", readonly=False)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure', required=True,
                                     domain="[('category_id', '=', product_uom_category_id)]")
    qty = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string="Unit Price", compute='_get_unit_price', store=True)
    discount = fields.Float(default=100.0, string='Discount')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    unit_total = fields.Monetary(string='Unit Total')
    sale_order_line = fields.Many2one(comodel_name='sale.order.line', string='Sale Order Line')
    free_type_type = fields.Selection(selection=[('standalone', 'Standalone'), ('embedded', 'Embedded')])

    @api.depends('product_tmpl_id', )
    @api.onchange('product_tmpl_id', )
    def _get_product_from_tmpl(self):
        self.product_id = self.product_tmpl_id.product_variant_id
        self.product_uom_id = self.product_tmpl_id.uom_id

    @api.depends('product_id', 'product_uom_id')
    def _get_unit_price(self):
        for record in self:
            product = record.product_id.with_context(
                lang=record.sale_order_id.partner_id.lang,
                partner=record.sale_order_id.partner_id,
                quantity=record.qty,
                date=record.sale_order_id.date_order,
                pricelist=record.sale_order_id.pricelist_id.id,
                uom=record.product_uom_id.id,
                fiscal_position=record.env.context.get('fiscal_position')
            )
            record.price_unit = product.price

    @api.onchange('qty', 'product_id', 'product_uom_id')
    def get_unit_price_total(self):
        for record in self:
            record.unit_total = record.qty * record.price_unit

    @api.model_create_multi
    def create(self, vals_list):
        sales_order = self.env['one.sale.order.free.product'].search(
            [('sale_order_id', '=', self._context['active_id'])])
        sales_order.unlink()
        res = super(SaleOrderFreeProduct, self).create(vals_list)
        for line in res:
            self.env['sale.order.line'].search([('is_free', '=', True), ('order_id', '=', line.sale_order_id.id), (
                'product_id', '=', line.product_id.id)]).unlink()
            new_line = self.env['sale.order.line'].create({
                'order_id': line.sale_order_id.id,
                'product_id': line.product_id.id,
                'price_unit': 0,
                'is_free': True,
                'product_uom_qty': line.qty,
            })
            line.write({'sale_order_line': new_line.id})
        return res


class SaleOrderFreeProductAddWizard(models.TransientModel):
    _name = 'one.sale.order.free.product.add.wizard'

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderFreeProductAddWizard, self).default_get(fields_list)
        sales_orders = self.env['one.sale.order.free.product'].search(
            [('sale_order_id', '=', self._context['active_id'])])
        vals = []
        for record in sales_orders:
            vals.append((0, 0, {
                'sale_order_id': record.sale_order_id.id,
                'product_tmpl_id': record.product_id.product_tmpl_id.id,
                'product_id': record.product_id.id,
                'product_uom_id': record.product_uom_id.id if record.product_uom_id else False,
                'qty': record.qty,
                'price_unit': record.price_unit,
                'discount': record.discount,
                'currency_id': record.currency_id.id if record.currency_id else False,
                'unit_total': record.unit_total,
            }))
        res.update({'sales_order_add_free_products': vals})
        return res

    sales_order_add_free_products = fields.One2many(comodel_name='one.sale.order.free.product', string='Products',
                                                    inverse_name='id')
    free_type_type = fields.Selection(selection=[('standalone', 'Standalone'), ('embedded', 'Embedded')], store=False)

    @api.model
    def create(self, vals_list):
        if 'sales_order_add_free_products' in vals_list:
            total_free = sum([x[-1]['unit_total'] for x in vals_list['sales_order_add_free_products']])
            sales_order = self.env['sale.order'].search([('id', '=', self._context['active_id'])])
            if sales_order.free_total:
                if sales_order.free_total < total_free:
                    raise ValidationError('free product total grate then invoice free total')
            else:
                raise ValidationError('free product total grate then invoice free total')
            return super(SaleOrderFreeProductAddWizard, self).create(vals_list)
        else:
            raise ValidationError('you must add one free product at least')
