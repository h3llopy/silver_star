from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OneCustomerTarget(models.Model):
    _name = 'one.customer.target'

    name = fields.Char(string='Name', required=True)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    target_amount = fields.Float(string='Target Amount')
    state = fields.Selection(selection=[('draft', 'Draft'), ('inprogress', 'In Progress'), ('expire', 'Expire')], default='draft')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company,
        index=True, required=True)
    line_ids = fields.One2many(comodel_name='one.customer.target.line', string='Lines', inverse_name='target_id', required=True)

    def confirm_run_customer_target(self):
        for record in self:
            if record.line_ids:
                record.state = 'inprogress'
            else:
                raise ValidationError('Can\'t run target without lines')

    def back_draft_customer_target(self):
        for record in self:
            record.state = 'draft'

    def apply_sale_target(self, move_type, stock_move):
        current_target = self.search(
            [('customer_id', '=', stock_move.partner_id.id), ('start_date', '<=', stock_move.date.date()),
             ('end_date', '>=', stock_move.date.date())],
            limit=1)
        inserted_vals = []
        if current_target:
            for line in stock_move.move_line_ids:
                current_target_line = current_target.line_ids.search(
                    [('target_id', '=', current_target.id), ('product_id', '=', line.product_id.id),('product_uom', '=', line.product_uom_id.id)], limit=1)
                sale_line_id = stock_move.sale_id.order_line.search(
                    [('order_id', '=', stock_move.sale_id.id), ('product_id', '=', line.product_id.id), ('product_uom', '=', line.product_uom_id.id)],limit=1)
                if current_target_line:
                    inserted_vals.append({
                        'target_id': current_target.id,
                        'target_line_id': current_target_line.id,
                        'customer_id': stock_move.partner_id.id,
                        'company_id': stock_move.company_id.id,
                        'product_id': line.product_id.id,
                        'product_template_id': line.product_id.product_tmpl_id.id,
                        'line_uom': line.product_uom_id.id,
                        'line_qty': (line.qty_done * 1) if move_type == 'sale' else (line.qty_done * -1),
                        'sale_order_id': stock_move.sale_id.id,
                        'sale_order_line_id': sale_line_id.id,
                        'sale_order_line_price_unit': sale_line_id.price_unit,
                        'salesman_id': stock_move.sale_id.user_id.id,
                        'sale_order_line_discount': sale_line_id.discount,
                        'sale_order_line_price_total': sale_line_id.price_subtotal,
                        'sold_percent_target': (((line.product_uom_qty * 10) / current_target_line.target_qty) * 10) if move_type == 'sale' else (((
                                                  line.product_uom_qty * 10) / current_target_line.target_qty) * 10) * -1,
                        'stock_move': stock_move.id,
                        'result_type': move_type
                    })
                if move_type == 'sale':
                    current_target_line.sold_qty += line.qty_done
                if move_type == 'return':
                    current_target_line.return_qty += line.qty_done
            return self.env['one.customer.target.result'].create(inserted_vals)


class OneCustomerTargetLine(models.Model):
    _name = 'one.customer.target.line'

    target_id = fields.Many2one(comodel_name='one.customer.target', string='Target', required=True)
    target_id_id = fields.Integer(related='target_id.id')
    target_id_state = fields.Selection(related='target_id.state')
    customer_id = fields.Many2one(comodel_name='res.partner', related='target_id.customer_id', string='Customer', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product',
        domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True, required=True)
    product_template_id = fields.Many2one(
        comodel_name='product.template', string='Product Template', readonly=False, domain=[('sale_ok', '=', True)], required=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string='UOM', domain="[('category_id', '=', product_uom_category_id)]", required=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    target_qty = fields.Float(string='Target qty', required=True)
    sold_qty = fields.Float(string='Sold qty', readonly=True)
    return_qty = fields.Float(string='Return qty', readonly=True)
    remain_qty = fields.Float(string='Remaining qty', compute='_compute_remain_qty')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='target_id.company_id')
    sell_line_ids = fields.One2many(comodel_name='one.customer.target.result', string='Sold Lines', inverse_name='target_line_id')

    def _compute_remain_qty(self):
        self.remain_qty = self.sold_qty - self.return_qty

    @api.depends('product_template_id')
    @api.onchange('product_template_id')
    def _get_product_from_tmpl(self):
        self.product_id = self.product_template_id.product_variant_id
        return {
            'domain': {
                'product_id': [('product_tmpl_id', '=', self.product_template_id.id)]
            }
        }

    @api.depends('product_id')
    @api.onchange('product_id')
    def _product_tmpl_domain_product(self):
        if self.product_template_id:
            self.product_template_id = self.product_template_id.id

    @api.constrains('product_id', 'product_uom')
    @api.depends('product_id', 'product_uom')
    @api.onchange('product_uom')
    def _onchange_product_uom(self):
        rest = self.target_id.line_ids - self
        for line in rest:
            if self.product_id == line.product_id:
                if self.product_uom == line.product_uom:
                    raise ValidationError('no dublicat')


class OneCustomerTargetResult(models.Model):
    _name = 'one.customer.target.result'
    _rec_name = 'product_id'

    target_id = fields.Many2one(comodel_name='one.customer.target', string='Target')
    target_line_id = fields.Many2one(comodel_name='one.customer.target.line', string='Target Line')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_template_id = fields.Many2one(comodel_name='product.template', string='Product Template')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string='SO Line')
    sale_order_line_price_unit = fields.Float(string='SO line unit price')
    sale_order_line_discount = fields.Float(string='SO line discount')
    line_uom = fields.Many2one(comodel_name='uom.uom', string='UOM', )
    line_qty = fields.Float(string='QTY', )
    sale_order_line_price_total = fields.Float(string='SO line total', )
    salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman')
    sold_percent_target = fields.Float(string='Sold %/target')
    stock_move = fields.Many2one(comodel_name='stock.picking', string='Stock Move')
    result_type = fields.Selection(selection=[('sale', 'Sale'), ('return', 'Return')], string='Type')
