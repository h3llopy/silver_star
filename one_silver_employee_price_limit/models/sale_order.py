#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / sale_order.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_have_limit = fields.Boolean(store=True)
    state = fields.Selection(selection_add=[
        ('need_approve', 'Need Approve'),
        ('approve', 'Approve'),

    ])
    can_confirm = fields.Boolean(string='Can Confirm', default=False, compute='_can_confirm_sales_order')
    need_approve = fields.Boolean(string='Need Approve', default=False, compute='_can_confirm_sales_order_line')
    sale_order_line_need_approve_count = fields.Integer(compute='_get_sale_order_lines_need_approve_count')

    def _get_user_limit_method(self):
        if self.env.user.user_limit_type == 'product_limit':
            return 'amount'
        else:
            return 'percent'

    user_limit_method = fields.Selection(selection=[('percent', '[%] Percent'), ('amount', '[$] Amount')],
                                         default=_get_user_limit_method)

    user_limit_type = fields.Selection(selection=[('user_limit', 'User Limit'), ('product_limit', 'Product Limit')],
                                       default=lambda self: self.env.user.user_limit_type, readonly=True)

    def unlink(self):
        for order in self:
            if order.state not in ('draft', 'cancel', 'need_approve'):
                raise UserError(
                    _('You can not delete a sent quotation or a confirmed sales order. You must first cancel it.'))
        return super(SaleOrder, self).unlink()

    def _can_confirm_sales_order(self):
        unstated_lines = []
        if self.order_line:
            for record in self.order_line:
                if record.need_approve == True and record.approve_done == False:
                    unstated_lines.append(record)
            if unstated_lines:
                self.can_confirm = True
            else:
                self.can_confirm = True
        else:
            self.can_confirm = False

    @api.depends('order_line')
    @api.onchange('order_line')
    def _can_confirm_sales_order_line(self):
        if self.partner_id and self.pricelist_id:
            unstated_lines = []
            if self.order_line:
                for record in self.order_line:
                    if record.need_approve == True and record.approve_done == False:
                        unstated_lines.append(record)
                if unstated_lines:
                    self.need_approve = True
                else:
                    self.need_approve = False
            else:
                self.need_approve = False
        else:
            self.need_approve = False

    @api.depends('partner_id', 'pricelist_id')
    @api.onchange('partner_id', 'pricelist_id')
    def _onchange_partner_id(self):
        self.order_line = [(6, 0, [])]

    @api.depends('pricelist_id', 'partner_id')
    @api.onchange('pricelist_id', 'partner_id')
    def _onchange_pricelist_id(self):

        if self.user_id.id in self.pricelist_id.employee_ids.user_id.ids or self.user_limit_type in ['user_limit',
                                                                                                     'product_limit']:
            self.user_have_limit = True
        else:
            self.user_have_limit = False

    def _get_sale_order_lines_need_approve_count(self):
        res = self.env['one.sale.order.line.need.approve'].search_count([('sale_order_id', '=', self.id)])
        self.sale_order_line_need_approve_count = res

    def get_sale_order_lines_need_approve(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lines Need Approve',
            'view_mode': 'tree',
            'res_model': 'one.sale.order.line.need.approve',
            'domain': [('sale_order_id', '=', self.id)],
            'context': "{'create': False}"
        }

    @api.depends('user_limit_method')
    @api.onchange('user_limit_method')
    def _onchange_user_limit_method(self):
        list_ids = []
        for record in self:
            if record.order_line:
                for line in record.order_line:
                    list_ids.append(
                        (1, line.id, {'price_unit': line.origin_price_unit, 'discount': 0.0, 'need_approve': False}))
        return self.update({'order_line': list_ids})


class SaleOrderLineNeedApprove(models.Model):
    _name = 'one.sale.order.line.need.approve'
    _sql_constraints = [
        ('unique_order_line', 'unique (sale_order_id, sale_order_line_id)', 'This order line already exists')
    ]
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sales Order', readonly=True, store=True)
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string='Sales Order Line', readonly=True,
                                         store=True, ondelete='set null')
    state = fields.Selection(selection=[('new', 'New'), ('approve', 'Approve'), ('reject', 'Reject')], readonly=True,
                             store=True, default='new')
    price_method = fields.Selection([('increase', '[+]Increase'), ('decrease', '[-]Decrease')])
    new_percent = fields.Integer(string='New %', default=0.0)
    new_amount = fields.Integer(string='New $', default=0.0)
    final_amount = fields.Integer(string='Unit Price', compute='_calculate_final_amount')
    product_id = fields.Many2one(string='Product', comodel_name='product.product', readonly=1)
    origin_price_unit = fields.Float(string='Origin Unit Price', related='sale_order_line_id.origin_price_unit')
    need_approve_price_unit = fields.Float(string='$ Need Approve', )
    need_approve_percent = fields.Float(string='% Need Approve', )
    pricelist_id = fields.Many2one(string='Price List', comodel_name='product.pricelist',
                                   related='sale_order_id.pricelist_id')
    create_by = fields.Many2one(string='Created By', comodel_name='res.users', related='sale_order_line_id.create_uid')
    user_have_limit = fields.Boolean(compute='_get_customer_limit', store=False)
    user_limit_method = fields.Selection(related='sale_order_id.user_limit_method')
    user_limit_type = fields.Selection(selection=[('user_limit', 'User Limit'), ('product_limit', 'Product Limit')], compute='_get_user_limit_type')
    cost_price = fields.Float(string='Cost', related='product_id.standard_price')
    profit_percent = fields.Float(string='Profit %', readonly=True, compute='_get_profit_percent')

    def _get_profit_percent(self):
        for record in self:
            if record.sale_order_id.user_limit_method == 'amount':
                record.profit_percent = (((record.need_approve_price_unit - record.product_id.standard_price) * 100) / record.product_id.standard_price)
            elif record.sale_order_id.user_limit_method == 'percent':
                if record.origin_price_unit != 0.0 and record.product_id.standard_price != 0.0:
                    record.profit_percent = (((record.origin_price_unit - ((record.origin_price_unit * record.need_approve_percent) / 100) - record.product_id.standard_price) * 100) / record.product_id.standard_price)
                else:
                    record.profit_percent = 0.0
            else:
                record.profit_percent = 0.0

    def _get_customer_limit(self):
        if self.env.uid in self.sale_order_id.pricelist_id.employee_ids.user_id.ids or self.user_limit_type in [
            'user_limit', 'product_limit']:
            self.user_have_limit = True
        else:
            self.user_have_limit = False

    def _get_user_limit_type(self):
        for line in self:
            line.user_limit_type = self.env.user.user_limit_type

    @api.depends('user_limit_method', 'new_percent', 'new_amount', 'price_method')
    def _calculate_final_amount(self):
        # if self.env.user.user_limit_type == 'user_limit':
        for record in self:
            if record.sale_order_id.user_limit_method == 'amount':
                if record.price_method == 'decrease':
                    record.final_amount = record.origin_price_unit - record.new_amount
                elif record.price_method == 'increase':
                    record.final_amount = record.origin_price_unit + record.new_amount
                else:
                    record.final_amount = record.need_approve_price_unit
            elif record.sale_order_id.user_limit_method == 'percent':
                if record.new_percent > 100:
                    raise ValidationError('Percentage must be 100% as maximum')
                else:
                    if record.price_method == 'decrease':
                        record.final_amount = record.origin_price_unit - (
                                (record.origin_price_unit * record.new_percent) / 100)
                    else:
                        record.final_amount = record.origin_price_unit + (
                                (record.origin_price_unit * record.new_percent) / 100)
            else:
                record.final_amount = record.need_approve_price_unit
        # else:
        #     raise ValidationError('You not have limit type to do it')

    def order_line_approve(self):
        final_state_approve = 'need_approve'
        for record in self:
            if record.user_have_limit:
                user_id = record.sale_order_id.pricelist_id.employee_ids.search([('user_id', '=', self.env.uid)])
                if self._context['action'] == 'approve':
                    if record.sale_order_id.user_limit_method == 'amount':
                        max_price_unit = record.origin_price_unit + user_id.search(
                            [('pricelist_id', '=', record.sale_order_id.pricelist_id.id),
                             ('user_id', '=', self.env.uid)]).increase_amount
                        min_price_unit = record.origin_price_unit - user_id.search(
                            [('pricelist_id', '=', record.sale_order_id.pricelist_id.id),
                             ('user_id', '=', self.env.uid)]).decrease_amount
                        if min_price_unit <= record.final_amount <= max_price_unit:

                            self.env['sale.order.line'].search([('order_id', '=', record.sale_order_id.id),
                                                                ('id', '=', record.sale_order_line_id.id)]).write({
                                'approve_done': True,
                                'price_unit': record.final_amount
                            })
                            record.state = 'approve'
                        else:
                            raise ValidationError('you exceed your limit')

                    if record.sale_order_id.user_limit_method == 'percent':

                        max_price_unit = record.origin_price_unit
                        min_price_unit = record.origin_price_unit - (
                                (record.origin_price_unit * user_id.search(
                                    [('pricelist_id', '=', record.sale_order_id.pricelist_id.id),
                                     ('user_id', '=', self.env.uid)]).decrease_percent) / 100)
                        if self._context['action'] == 'approve':
                            if min_price_unit <= record.origin_price_unit <= max_price_unit:
                                self.env['sale.order.line'].search([('order_id', '=', record.sale_order_id.id),
                                                                    ('id', '=', record.sale_order_line_id.id)]).write({
                                    'approve_done': True,
                                    'discount': record.new_percent

                                })
                                record.state = 'approve'
                            else:
                                raise ValidationError('you exceed your limit')
                elif self._context['action'] == 'reject':
                    self.env['sale.order.line'].search([('order_id', '=', record.sale_order_id.id),
                                                        ('id', '=', record.sale_order_line_id.id)]).unlink()
                    record.state = 'reject'
                    record.sale_order_line_id = False
                else:
                    pass

        if not self.env['one.sale.order.line.need.approve'].search(
                [('state', '=', 'new'), ('sale_order_id', '=', self._context['active_id'])]):
            final_state_approve = 'approve'
        self.env['sale.order'].search([('id', '=', self._context['active_id'])]).state = final_state_approve


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    user_have_limit = fields.Boolean(store=False, related='order_id.user_have_limit')
    user_limit_method = fields.Selection(related='order_id.user_limit_method')
    user_limit_type = fields.Selection(related='order_id.user_limit_type')
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', store=False, related='order_id.pricelist_id')
    need_approve = fields.Boolean(string='Need Approve', default=False, compute='_get_over_limit_approve_state',
                                  store=True)
    approve_done = fields.Boolean(string='Approved', default=False)
    origin_price_unit = fields.Float(string='Origin Unit Price', required=True, digits='Product Price',
                                     compute='_get_origin_price_unit')

    @api.depends('product_template_id', )
    @api.onchange('product_template_id', )
    def _get_origin_price_unit(self):
        for record in self:
            if record.order_id.pricelist_id:
                product = record.product_id.with_context(
                    lang=record.order_id.partner_id.lang,
                    partner=record.order_id.partner_id,
                    quantity=record.product_uom_qty,
                    date=record.order_id.date_order,
                    pricelist=record.order_id.pricelist_id.id,
                    uom=record.product_uom.id,
                    fiscal_position=record.env.context.get('fiscal_position')
                )
                if product:
                    record.origin_price_unit = self.env['account.tax']._fix_tax_included_price_company(
                        record._get_display_price(product), product.taxes_id, record.tax_id, record.company_id)
                else:
                    record.origin_price_unit = 0.0
            else:
                raise ValidationError('Select Partner/Price List First')

    @api.onchange('price_unit', 'discount','product_uom')
    def _get_over_limit_approve_state(self):
        for record in self:
            if record.product_template_id or record.product_id:
                if record.order_id.user_limit_type == 'user_limit':
                    user_id = record.order_id.pricelist_id.employee_ids.search(
                        [('pricelist_id', '=', record.order_id.pricelist_id.id), ('user_id', '=', self.env.uid)])
                    if record.order_id.user_limit_method == 'amount':
                        max_price_unit = record.origin_price_unit + user_id.search(
                            [('pricelist_id', '=', record.order_id.pricelist_id.id),
                             ('user_id', '=', self.env.uid)]).increase_amount
                        min_price_unit = record.origin_price_unit - user_id.search(
                            [('pricelist_id', '=', record.order_id.pricelist_id.id),
                             ('user_id', '=', self.env.uid)]).decrease_amount
                        if min_price_unit < record.price_unit < max_price_unit:
                            record.need_approve = False
                        else:
                            record.need_approve = True
                    elif record.order_id.user_limit_method == 'percent':
                        max_price_unit = record.origin_price_unit
                        min_price_unit = record.origin_price_unit - (
                                (record.origin_price_unit * user_id.search(
                                    [('pricelist_id', '=', record.order_id.pricelist_id.id),
                                     ('user_id', '=', self.env.uid)]).decrease_percent) / 100)
                        if min_price_unit <= (record.price_subtotal / record.product_uom_qty) <= max_price_unit:
                            record.need_approve = False
                        else:
                            record.need_approve = True

                    else:
                        record.need_approve = False
                elif record.order_id.user_limit_type == 'product_limit':
                    min_price = record.pricelist_id.item_ids.get_min_price(record)
                    if min_price:
                        if record.product_id.uom_id.uom_type == 'bigger':
                            if record.product_uom.uom_type == 'reference':
                                min_price = min_price / record.product_id.uom_id.factor_inv
                            if record.product_uom.uom_type == 'smaller':
                                min_price = (min_price / record.product_id.uom_id.factor_inv) * record.product_uom.factor_inv
                        if record.product_id.uom_id.uom_type == 'smaller':
                            if record.product_uom.uom_type == 'reference':
                                min_price = min_price * record.product_id.uom_id.factor
                            if record.product_uom.uom_type == 'bigger':
                                min_price = (min_price * record.product_id.uom_id.factor) * record.product_uom.factor_inv
                        if record.product_id.uom_id.uom_type == 'reference':
                            if record.product_uom.uom_type == 'smaller':
                                min_price = min_price / record.product_uom.factor
                            elif record.product_uom.uom_type == 'bigger':
                                min_price = min_price * record.product_uom.factor_inv
                        else:
                            min_price = min_price
                    else:
                        min_price = record.product_template_id.min_list_price

                    if min_price <= record.price_unit:
                        record.need_approve = False
                    else:
                        record.need_approve = True
                else:
                    record.need_approve = False
            else:
                record.need_approve = False

    @api.depends('product_uom')
    @api.onchange('product_uom')
    def _onchanege_product_uom(self):
        for record in self:
            product = record.product_id.with_context(
                lang=record.order_id.partner_id.lang,
                partner=record.order_id.partner_id,
                quantity=record.product_uom_qty,
                date=record.order_id.date_order,
                pricelist=record.order_id.pricelist_id.id,
                uom=record.product_uom.id,
                fiscal_position=record.env.context.get('fiscal_position')
            )
            if product:
                record.origin_price_unit = self.env['account.tax']._fix_tax_included_price_company(
                record._get_display_price(product), product.taxes_id, record.tax_id, record.company_id)
            else:
                record.origin_price_unit = 0.0
