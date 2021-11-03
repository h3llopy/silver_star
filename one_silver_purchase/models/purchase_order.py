""" Initialize Purchase Order """
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(
        selection_add=[('shipped', 'Shipped From Supplier'),
                       ('inside_port', 'Inside The Port'),
                       ('outside_port', 'Outside The Port')]
    )
    shipping_type = fields.Selection(
        related='partner_id.shipping_type'
    )

    deadline_user_reminder_email = fields.Boolean()
    deadline_user_reminder_email_days = fields.Integer()
    deadline_user_reminder_email_notify_sort = fields.Selection(selection=[('before', 'Before'), ('after', 'After')])
    deadline_percent = fields.Float(string='Deadline Percent', default=100)
    deadline_percent_amount = fields.Float(string='Deadline Percent Amount', default=0.0)
    deadline_one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')

    receipt_user_reminder_email = fields.Boolean()
    receipt_user_reminder_email_days = fields.Integer()
    receipt_user_reminder_email_notify_sort = fields.Selection(selection=[('before', 'Before'), ('after', 'After')])
    receipt_percent = fields.Float(string='Receipt Percent', default=0)
    receipt_percent_amount = fields.Float(string='Receipt Percent Amount', default=0.0)
    receipt_one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')

    shipping_date = fields.Datetime()
    shipping_date_reminder_email = fields.Boolean()
    shipping_date_reminder_email_days = fields.Integer()
    shipping_date_reminder_email_notify_sort = fields.Selection(selection=[('before', 'Before'), ('after', 'After')])
    shipping_percent = fields.Float(string='shipping Percent', default=0)
    shipping_percent_amount = fields.Float(string='shipping Percent Amount', default=0.0)
    shipping_one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')

    inside_port_date = fields.Datetime()
    inside_port_date_reminder_email = fields.Boolean()
    inside_port_date_reminder_email_days = fields.Integer()
    inside_port_date_reminder_email_notify_sort = fields.Selection(selection=[('before', 'Before'), ('after', 'After')])
    inside_port_percent = fields.Float(string='inside port Percent', default=0)
    inside_port_percent_amount = fields.Float(string='inside port Percent Amount', default=0.0)
    inside_port_one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')

    outside_port_date = fields.Datetime(string="Order Date")
    outside_port_date_reminder_email = fields.Boolean()
    outside_port_date_reminder_email_days = fields.Integer()
    outside_port_date_reminder_email_notify_sort = fields.Selection(selection=[('before', 'Before'), ('after', 'After')])
    outside_port_percent = fields.Float(string='Order Date Percent', default=0)
    outside_port_percent_amount = fields.Float(string='Order Date Percent Amount', default=0.0)
    outside_port_one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')

    landed_cost_count = fields.Integer(compute='_po_landed_cost_count')

    partner_ref_date = fields.Date(string='Vendor Reference Date')
    shipping_via = fields.Many2one(comodel_name='res.partner', string='Shipping via')
    def shipped_from_supplier(self):
        """ move to shipped"""
        if not self.shipping_date:
            raise ValidationError(_("Please Enter Shipping Date"))
        else:
            self.state = 'shipped'

    def port_has_been_reached(self):
        """ move to inside port"""
        if not self.inside_port_date:
            raise ValidationError(_("Please Enter Inside Port Date"))
        else:
            self.state = 'inside_port'

    def extracted_from_the_port(self):
        """ move to outside port"""
        if not self.outside_port_date:
            raise ValidationError(_("Please Enter Outside Port Date"))
        else:
            self.state = 'outside_port'

    @api.depends('state', 'order_line.qty_to_invoice')
    def _get_invoiced(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for order in self:
            if order.state not in ('purchase', 'done', 'shipped', 'inside_port', 'outside_port'):
                order.invoice_status = 'no'
                continue

            if any(
                    not float_is_zero(line.qty_to_invoice, precision_digits=precision)
                    for line in order.order_line.filtered(lambda l: not l.display_type)
            ):
                order.invoice_status = 'to invoice'
            elif (
                    all(
                        float_is_zero(line.qty_to_invoice, precision_digits=precision)
                        for line in order.order_line.filtered(lambda l: not l.display_type)
                    )
                    and order.invoice_ids
            ):
                order.invoice_status = 'invoiced'
            else:
                order.invoice_status = 'no'

    @api.model
    def create(self, vals_list):
        deadline_percent = vals_list['deadline_percent'] if 'deadline_percent' in vals_list else 100.0
        receipt_percent = vals_list['receipt_percent'] if 'receipt_percent' in vals_list else 100.0
        shipping_percent = vals_list['shipping_percent'] if 'shipping_percent' in vals_list else 0.0
        inside_port_percent = vals_list['inside_port_percent'] if 'inside_port_percent' in vals_list else 0.0
        outside_port_percent = vals_list['outside_port_percent'] if 'outside_port_percent' in vals_list else 0.0

        percent = deadline_percent + receipt_percent + shipping_percent + inside_port_percent + outside_port_percent
        if percent != 100:
            raise ValidationError('Payment Percent for all stages must be 100%')
        else:
            res = super(PurchaseOrder, self).create(vals_list)
            if res.shipping_type == 'external':
                res.deadline_percent_amount = ((res.amount_total * res.deadline_percent) / 100)
                res.receipt_percent_amount = ((res.amount_total * res.receipt_percent) / 100)
                res.shipping_percent_amount = ((res.amount_total * res.receipt_percent) / 100)
                res.inside_port_percent_amount = ((res.amount_total * res.receipt_percent) / 100)
                res.outside_port_percent_amount = ((res.amount_total * res.receipt_percent) / 100)
                self.env['purchase.order.payment.schedule'].set_schedule_percent(po_obj=res, apply_to='all')
            return res

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        if self.shipping_type == 'external':
            self.env['purchase.order.payment.schedule'].update_schedule_percent(po_obj=self, vals=vals)
        return res

    def get_related_po_landed_cost(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Landed Cost',
            'view_mode': 'tree',
            'res_model': 'account.move',
            'domain': [('land_cost_purchase_order_ids', 'in', self.id)],
            'context': "{'create': False}"
        }

    def _po_landed_cost_count(self):
        for record in self:
            record.landed_cost_count = self.env['account.move'].search_count([('land_cost_purchase_order_ids', 'in', self.id)])

    def _select(self):
        res = super()._select()
        res += ", (CASE WHEN po.receipt_percent_amount IS NOT NULL THEN po.receipt_percent_amount ELSE 0.0 END) AS receipt_percent_amount"
        res += ", (CASE WHEN po.shipping_percent_amount IS NOT NULL THEN po.shipping_percent_amount ELSE 0.0 END) AS shipping_percent_amount"
        res += ", (CASE WHEN po.inside_port_percent_amount IS NOT NULL THEN po.inside_port_percent_amount ELSE 0.0 END) AS inside_port_percent_amount"
        res += ", (CASE WHEN po.outside_port_percent_amount IS NOT NULL THEN po.outside_port_percent_amount ELSE 0.0 END) AS outside_port_percent_amount"
        return res

    def _group_by(self):
        return super()._group_by() + ",receipt_percent_amount, shipping_percent_amount,inside_port_percent_amount,outside_port_percent_amount "


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    list_price = fields.Float(compute='_compute_min_price', )
    min_list_price = fields.Float(compute='_compute_min_price', )
    expire_date = fields.Date(compute='_compute_expire_date')
    prod_expire_date = fields.Date(compute='_compute_expire_date')
    unit_ratio = fields.Float(string='Unit Raito', compute='_compute_min_price', )
    unit_lc_cost = fields.Float(compute='_compute_lc_cost', )

    def _compute_min_price(self):
        for line in self:
            line.list_price = line.product_id.list_price if line.product_id.list_price else 0.0
            line.min_list_price = line.product_id.min_list_price if line.product_id.min_list_price else 0.0
            line.unit_ratio = line.product_uom.factor_inv

    def _compute_expire_date(self):
        for line in self:
            product_stock_move = self.env['stock.move'].search([('purchase_line_id', '=', line.id), ('product_id', '=', line.product_id.id)], limit=1,
                                                               order='date asc')
            product_stock_move_line = self.env['stock.move.line'].search([('id', 'in', product_stock_move.move_line_ids.ids)], limit=1,
                                                                         order='date asc')
            line.expire_date = product_stock_move_line.expiration_date
            line.prod_expire_date = product_stock_move_line.production_exp_date

    def _compute_lc_cost(self):
        for line in self:
            product_stock_move = self.env['stock.move'].search([('purchase_line_id', '=', line.id), ('product_id', '=', line.product_id.id)], limit=1,
                                                               order='date asc')
            if product_stock_move:
                product_stock_move_line = self.env['stock.move.line'].search([('id', 'in', product_stock_move.move_line_ids.ids)], limit=1,
                                                                             order='date asc')
                if product_stock_move_line:
                    product_stock_pick_line = self.env['stock.picking'].search(
                        [('move_line_ids', 'in', product_stock_move_line.ids), ('product_id', '=', line.product_id.id),
                         ('purchase_id', '=', line.order_id.id)], limit=1,
                        order='date_done asc')
                    if product_stock_pick_line:
                        product_stock_lc = self.env['stock.landed.cost'].search([('picking_ids', 'in', product_stock_pick_line.ids)], limit=1,
                                                                                order='date asc')
                        if product_stock_lc:
                            product_stock_lc_line = self.env['stock.valuation.adjustment.lines'].search(
                                [('cost_id', 'in', product_stock_lc.ids), ('product_id', '=', line.product_id.id)])
                            if product_stock_lc_line:
                                lc_sum = []
                                for slc in product_stock_lc_line:
                                    lc_sum.append(slc.final_cost)
                                line.unit_lc_cost = sum(lc_sum)
                            else:
                                line.unit_lc_cost = 0.0
                        else:
                            line.unit_lc_cost = 0.0
                    else:
                        line.unit_lc_cost = 0.0
                else:
                    line.unit_lc_cost = 0.0
            else:
                line.unit_lc_cost = 0.0

class OnePaymentMethods(models.Model):
    _name = 'one.payment.method'
    name = fields.Char(string='Name')
    company_id = fields.Many2one(string="Company", comodel_name='res.company', default=lambda self: self.env.company.id)


class PurchaseOrderPaymentsSchedule(models.Model):
    _name = 'purchase.order.payment.schedule'
    purchase_order_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
    vendor_id = fields.Many2one(comodel_name='res.partner', related='purchase_order_id.partner_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='purchase_order_id.currency_id', store=True)
    one_payment_method = fields.Many2one(comodel_name='one.payment.method', string='Payment Method')
    action_type = fields.Selection(
        selection=[('receipt', 'Receipt'), ('shipping', 'Shipping'), ('inside_port', 'Inside Port'), ('outside_port', 'Outside Port'),
                   ('deadline', 'Order Deadline')])
    action_date = fields.Date(string='Date')
    schedule_date = fields.Date(string='Schedule Date')
    action_percent = fields.Float(string='Percent')
    action_amount = fields.Float(string='Amount')
    payment_status = fields.Selection(selection=[('unpaid', 'UnPaid'), ('paid', 'Paid')], string='Payment Status', default='unpaid')
    activity_id = fields.Many2one('mail.activity', 'Linked Activity', )

    def set_schedule_percent(self, po_obj, apply_to):
        if apply_to in ['all', 'deadline']:
            if po_obj.date_order and po_obj.deadline_user_reminder_email:
                date_order_date_deadline = po_obj.date_order + relativedelta(
                    days=(po_obj.deadline_user_reminder_email_days * -1) if po_obj.deadline_user_reminder_email_notify_sort == 'before' else (
                            po_obj.deadline_user_reminder_email_days * 1))
                new_sch = self.create({
                    'purchase_order_id': po_obj.id,
                    'one_payment_method': po_obj.deadline_one_payment_method.id,
                    'action_type': 'deadline',
                    'action_date': po_obj.date_order,
                    'schedule_date': date_order_date_deadline,
                    'action_percent': po_obj.deadline_percent,
                    'action_amount': ((po_obj.amount_total * po_obj.deadline_percent) / 100),
                    'payment_status': 'unpaid',
                })
                po_deadline_date_activity = po_obj.activity_schedule(
                    'purchase.po_deadline_date',
                    summary=_("Deadline Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Deadline Date : {} \n With payment : {}'.format(date_order_date_deadline,
                                                                          ((po_obj.amount_total * po_obj.deadline_percent) / 100)),
                    date_deadline=date_order_date_deadline,
                    activity_type_id=self.env.ref('one_silver_purchase.po_deadline_date', raise_if_not_found=False).id
                )
                new_sch.activity_id = po_deadline_date_activity.id
        if apply_to in ['all', 'receipt']:
            if po_obj.date_planned and po_obj.receipt_user_reminder_email:
                date_planned_date_deadline = po_obj.date_planned + relativedelta(
                    days=(po_obj.receipt_user_reminder_email_days * -1) if po_obj.receipt_user_reminder_email_notify_sort == 'before' else (
                            po_obj.receipt_user_reminder_email_days * 1))
                new_sch = self.create({
                    'purchase_order_id': po_obj.id,
                    'one_payment_method': po_obj.receipt_one_payment_method.id,
                    'action_type': 'receipt',
                    'action_date': po_obj.date_planned,
                    'schedule_date': date_planned_date_deadline,
                    'action_percent': po_obj.receipt_percent,
                    'action_amount': ((po_obj.amount_total * po_obj.receipt_percent) / 100),
                    'payment_status': 'unpaid',
                })
                po_receipt_date_activity = po_obj.activity_schedule(
                    'purchase.po_receipt_date',
                    summary=_("Receipt Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Receipt Date : {} \n With payment : {}'.format(date_planned_date_deadline,
                                                                         ((po_obj.amount_total * po_obj.receipt_percent) / 100)),
                    date_deadline=date_planned_date_deadline,
                    activity_type_id=self.env.ref('one_silver_purchase.po_receipt_date', raise_if_not_found=False).id
                )
                new_sch.activity_id = po_receipt_date_activity.id
        if apply_to in ['all', 'shipping']:
            if po_obj.shipping_date and po_obj.shipping_date_reminder_email:
                shipping_date_date_deadline = po_obj.shipping_date + relativedelta(
                    days=(po_obj.shipping_date_reminder_email_days * -1) if po_obj.shipping_date_reminder_email_notify_sort == 'before' else (
                            po_obj.shipping_date_reminder_email_days * 1))
                new_sch = self.create({
                    'purchase_order_id': po_obj.id,
                    'one_payment_method': po_obj.shipping_one_payment_method.id,
                    'action_type': 'shipping',
                    'action_date': po_obj.shipping_date,
                    'schedule_date': shipping_date_date_deadline,
                    'action_percent': po_obj.shipping_percent,
                    'action_amount': ((po_obj.amount_total * po_obj.shipping_percent) / 100),
                    'payment_status': 'unpaid',
                })
                po_shipping_date_activity = po_obj.activity_schedule(
                    'purchase.po_shipping_date',
                    summary=_("Shipping Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Shipping Date : {} \n With payment : {}'.format(shipping_date_date_deadline,
                                                                          ((po_obj.amount_total * po_obj.shipping_percent) / 100)),
                    date_deadline=shipping_date_date_deadline,
                    activity_type_id=self.env.ref('one_silver_purchase.po_shipping_date', raise_if_not_found=False).id
                )
                new_sch.activity_id = po_shipping_date_activity.id
        if apply_to in ['all', 'inside_port']:
            if po_obj.inside_port_date and po_obj.inside_port_date_reminder_email:
                po_inside_port_date_date_deadline = po_obj.inside_port_date + relativedelta(
                    days=(po_obj.inside_port_date_reminder_email_days * -1) if po_obj.inside_port_date_reminder_email_notify_sort == 'before' else (
                            po_obj.inside_port_date_reminder_email_days * 1))
                new_sch = self.create({
                    'purchase_order_id': po_obj.id,
                    'one_payment_method': po_obj.inside_port_one_payment_method.id,
                    'action_type': 'inside_port',
                    'action_date': po_obj.inside_port_date,
                    'schedule_date': po_inside_port_date_date_deadline,
                    'action_percent': po_obj.inside_port_percent,
                    'action_amount': ((po_obj.amount_total * po_obj.inside_port_percent) / 100),
                    'payment_status': 'unpaid',
                })
                po_inside_port_date_activity = po_obj.activity_schedule(
                    'purchase.po_inside_port_date',
                    summary=_("Inside Port Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Inside Port Date : {} \n With payment : {}'.format(po_inside_port_date_date_deadline,
                                                                             ((po_obj.amount_total * po_obj.inside_port_percent) / 100)),
                    date_deadline=po_inside_port_date_date_deadline,
                    activity_type_id=self.env.ref('one_silver_purchase.po_inside_port_date', raise_if_not_found=False).id
                )
                new_sch.activity_id = po_inside_port_date_activity.id
        if apply_to in ['all', 'outside_port']:
            if po_obj.outside_port_date and po_obj.outside_port_date_reminder_email:
                po_outside_port_date_deadline = po_obj.outside_port_date + relativedelta(
                    days=(po_obj.outside_port_date_reminder_email_days * -1) if po_obj.outside_port_date_reminder_email_notify_sort == 'before' else (
                            po_obj.outside_port_date_reminder_email_days * 1))
                new_sch = self.create({
                    'purchase_order_id': po_obj.id,
                    'one_payment_method': po_obj.outside_port_one_payment_method.id,
                    'action_type': 'outside_port',
                    'action_date': po_obj.outside_port_date,
                    'schedule_date': po_outside_port_date_deadline,
                    'action_percent': po_obj.outside_port_percent,
                    'action_amount': ((po_obj.amount_total * po_obj.outside_port_percent) / 100),
                    'payment_status': 'unpaid',
                })
                po_outside_port_date_activity = po_obj.activity_schedule(
                    'purchase.po_outside_port_date',
                    summary=_("Outside Port Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Outside Port Date : {} \n With payment : {}'.format(po_outside_port_date_deadline,
                                                                              ((po_obj.amount_total * po_obj.outside_port_percent) / 100)),
                    date_deadline=po_outside_port_date_deadline,
                    activity_type_id=self.env.ref('one_silver_purchase.po_outside_port_date', raise_if_not_found=False).id
                )
                new_sch.activity_id = po_outside_port_date_activity.id
        return True

    def update_schedule_percent(self, po_obj, vals):
        sched_pay_obj = self.search([('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid')])
        if sched_pay_obj:
            if 'date_order' in vals or 'deadline_user_reminder_email_days' in vals or 'deadline_user_reminder_email_notify_sort' in vals or 'deadline_percent' in vals or 'deadline_one_payment_method' in vals:
                re_date_order = datetime.strptime(vals['date_order'], '%Y-%m-%d %H:%M:%S') if 'date_order' in vals else po_obj.date_order
                re_deadline_user_reminder_email_days = vals[
                    'deadline_user_reminder_email_days'] if 'deadline_user_reminder_email_days' in vals else po_obj.deadline_user_reminder_email_days
                re_deadline_user_reminder_email_notify_sort = vals[
                    'deadline_user_reminder_email_notify_sort'] if 'deadline_user_reminder_email_notify_sort' in vals else po_obj.deadline_user_reminder_email_notify_sort
                re_deadline_percent = vals['deadline_percent'] if 'deadline_percent' in vals else po_obj.deadline_percent
                re_date_order_date_deadline = re_date_order + relativedelta(
                    days=(re_deadline_user_reminder_email_days * -1) if re_deadline_user_reminder_email_notify_sort == 'before' else (
                            re_deadline_user_reminder_email_days * 1))
                deadline_sched_pay_obj = sched_pay_obj.search(
                    [('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid'), ('action_type', '=', 'deadline')])
                deadline_sched_pay_obj.write({
                    'one_payment_method': vals[
                        'deadline_one_payment_method'] if 'deadline_one_payment_method' in vals else po_obj.deadline_one_payment_method.id,
                    'action_date': vals['date_order'] if 'date_order' in vals else po_obj.date_order,
                    'schedule_date': re_date_order_date_deadline,
                    'action_percent': re_deadline_percent,
                    'action_amount': ((po_obj.amount_total * re_deadline_percent) / 100),
                })
                deadline_sched_pay_obj.activity_id.action_done()
                po_deadline_date_activity = po_obj.activity_schedule(
                    'purchase.po_deadline_date',
                    summary=_("Deadline Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Deadline Date : {} \n With payment : {}'.format(deadline_sched_pay_obj.schedule_date, deadline_sched_pay_obj.action_amount),
                    date_deadline=deadline_sched_pay_obj.schedule_date,
                    activity_type_id=self.env.ref('one_silver_purchase.po_deadline_date', raise_if_not_found=False).id
                )
                deadline_sched_pay_obj.activity_id = po_deadline_date_activity.id
            if 'date_planned' in vals or 'receipt_user_reminder_email_days' in vals or 'receipt_user_reminder_email_notify_sort' in vals or 'receipt_percent' in vals or 'receipt_one_payment_method' in vals:
                re_date_planned = datetime.strptime(vals['date_planned'], '%Y-%m-%d %H:%M:%S') if 'date_planned' in vals else po_obj.date_planned
                re_receipt_user_reminder_email_days = vals[
                    'receipt_user_reminder_email_days'] if 'receipt_user_reminder_email_days' in vals else po_obj.receipt_user_reminder_email_days
                re_receipt_user_reminder_email_notify_sort = vals[
                    'receipt_user_reminder_email_notify_sort'] if 'receipt_user_reminder_email_notify_sort' in vals else po_obj.receipt_user_reminder_email_notify_sort
                re_receipt_percent = vals['receipt_percent'] if 'receipt_percent' in vals else po_obj.receipt_percent
                re_date_planned_date_deadline = re_date_planned + relativedelta(
                    days=(re_receipt_user_reminder_email_days * -1) if re_receipt_user_reminder_email_notify_sort == 'before' else (
                            re_receipt_user_reminder_email_days * 1))
                receipt_sched_pay_obj = sched_pay_obj.search(
                    [('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid'), ('action_type', '=', 'receipt')])
                receipt_sched_pay_obj.write({
                    'one_payment_method': vals[
                        'receipt_one_payment_method'] if 'receipt_one_payment_method' in vals else po_obj.receipt_one_payment_method.id,
                    'action_date': vals['date_planned'] if 'date_planned' in vals else po_obj.date_planned,
                    'schedule_date': re_date_planned_date_deadline,
                    'action_percent': re_receipt_percent,
                    'action_amount': ((po_obj.amount_total * re_receipt_percent) / 100),
                })
                receipt_sched_pay_obj.activity_id.action_done()
                po_receipt_date_activity = po_obj.activity_schedule(
                    'purchase.po_receipt_date',
                    summary=_("Receipt Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Receipt Date : {} \n With payment : {}'.format(receipt_sched_pay_obj.schedule_date, receipt_sched_pay_obj.action_amount),
                    date_deadline=receipt_sched_pay_obj.schedule_date,
                    activity_type_id=self.env.ref('one_silver_purchase.po_receipt_date', raise_if_not_found=False).id
                )
                receipt_sched_pay_obj.activity_id = po_receipt_date_activity.id
            if 'shipping_date' in vals or 'shipping_date_reminder_email_days' in vals or 'shipping_date_reminder_email_notify_sort' in vals or 'shipping_percent' in vals or 'shipping_one_payment_method' in vals:
                re_shipping_date = datetime.strptime(vals['shipping_date'], '%Y-%m-%d %H:%M:%S') if 'shipping_date' in vals else po_obj.shipping_date
                re_shipping_date_reminder_email_days = vals[
                    'shipping_date_reminder_email_days'] if 'shipping_date_reminder_email_days' in vals else po_obj.shipping_date_reminder_email_days
                re_shipping_date_reminder_email_notify_sort = vals[
                    'shipping_date_reminder_email_notify_sort'] if 'shipping_date_reminder_email_notify_sort' in vals else po_obj.shipping_date_reminder_email_notify_sort
                re_shipping_percent = vals['shipping_percent'] if 'shipping_percent' in vals else po_obj.shipping_percent
                re_shipping_date_deadline = re_shipping_date + relativedelta(
                    days=(re_shipping_date_reminder_email_days * -1) if re_shipping_date_reminder_email_notify_sort == 'before' else (
                            re_shipping_date_reminder_email_days * 1))
                shipping_sched_pay_obj = sched_pay_obj.search(
                    [('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid'), ('action_type', '=', 'shipping')])
                shipping_sched_pay_obj.write({
                    'one_payment_method': vals[
                        'shipping_one_payment_method'] if 'shipping_one_payment_method' in vals else po_obj.shipping_one_payment_method.id,
                    'action_date': vals['shipping_date'] if 'shipping_date' in vals else po_obj.shipping_date,
                    'schedule_date': re_shipping_date_deadline,
                    'action_percent': re_shipping_percent,
                    'action_amount': ((po_obj.amount_total * re_shipping_percent) / 100),
                })
                shipping_sched_pay_obj.activity_id.action_done()
                po_shipping_date_activity = po_obj.activity_schedule(
                    'purchase.po_shipping_date',
                    summary=_("Shipping Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Shipping Date : {} \n With payment : {}'.format(shipping_sched_pay_obj.schedule_date, shipping_sched_pay_obj.action_amount),
                    date_deadline=shipping_sched_pay_obj.schedule_date,
                    activity_type_id=self.env.ref('one_silver_purchase.po_shipping_date', raise_if_not_found=False).id
                )
                shipping_sched_pay_obj.activity_id = po_shipping_date_activity.id
            if 'inside_port_date' in vals or 'inside_port_date_reminder_email_days' in vals or 'inside_port_date_reminder_email_notify_sort' in vals or 'inside_port_percent' in vals or 'inside_port_one_payment_method' in vals:
                re_inside_port_date = datetime.strptime(vals['inside_port_date'],
                                                        '%Y-%m-%d %H:%M:%S') if 'inside_port_date' in vals else po_obj.inside_port_date
                re_inside_port_date_reminder_email_days = vals[
                    'inside_port_date_reminder_email_days'] if 'inside_port_date_reminder_email_days' in vals else po_obj.inside_port_date_reminder_email_days
                re_inside_port_date_reminder_email_notify_sort = vals[
                    'inside_port_date_reminder_email_notify_sort'] if 'inside_port_date_reminder_email_notify_sort' in vals else po_obj.inside_port_date_reminder_email_notify_sort
                re_inside_port_percent = vals['inside_port_percent'] if 'inside_port_percent' in vals else po_obj.inside_port_percent
                re_inside_port_date_deadline = re_inside_port_date + relativedelta(
                    days=(re_inside_port_date_reminder_email_days * -1) if re_inside_port_date_reminder_email_notify_sort == 'before' else (
                            re_inside_port_date_reminder_email_days * 1))
                inside_port_sched_pay_obj = sched_pay_obj.search(
                    [('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid'), ('action_type', '=', 'inside_port')])
                inside_port_sched_pay_obj.write({
                    'one_payment_method': vals[
                        'inside_port_one_payment_method'] if 'inside_port_one_payment_method' in vals else po_obj.inside_port_one_payment_method.id,
                    'action_date': vals['inside_port_date'] if 'inside_port_date' in vals else po_obj.inside_port_date,
                    'schedule_date': re_inside_port_date_deadline,
                    'action_percent': re_inside_port_percent,
                    'action_amount': ((po_obj.amount_total * re_inside_port_percent) / 100),
                })
                inside_port_sched_pay_obj.activity_id.action_done()
                po_inside_port_date_activity = po_obj.activity_schedule(
                    'purchase.po_inside_port_date',
                    summary=_("Inside Port Date Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Inside Port Date : {} \n With payment : {}'.format(inside_port_sched_pay_obj.schedule_date,
                                                                             inside_port_sched_pay_obj.action_amount),
                    date_deadline=inside_port_sched_pay_obj.schedule_date,
                    activity_type_id=self.env.ref('one_silver_purchase.po_inside_port_date', raise_if_not_found=False).id
                )
                inside_port_sched_pay_obj.activity_id = po_inside_port_date_activity.id
            if 'outside_port_date' in vals or 'outside_port_date_reminder_email_days' in vals or 'outside_port_date_reminder_email_notify_sort' in vals or 'outside_port_percent' in vals or 'outside_port_one_payment_method' in vals:
                re_outside_port_date = datetime.strptime(vals['outside_port_date'],
                                                         '%Y-%m-%d %H:%M:%S') if 'outside_port_date' in vals else po_obj.outside_port_date
                re_outside_port_date_reminder_email_days = vals[
                    'outside_port_date_reminder_email_days'] if 'outside_port_date_reminder_email_days' in vals else po_obj.outside_port_date_reminder_email_days
                re_outside_port_date_reminder_email_notify_sort = vals[
                    'outside_port_date_reminder_email_notify_sort'] if 'outside_port_date_reminder_email_notify_sort' in vals else po_obj.outside_port_date_reminder_email_notify_sort
                re_outside_port_percent = vals['outside_port_percent'] if 'outside_port_percent' in vals else po_obj.outside_port_percent
                re_outside_port_date_deadline = re_outside_port_date + relativedelta(
                    days=(re_outside_port_date_reminder_email_days * -1) if re_outside_port_date_reminder_email_notify_sort == 'before' else (
                            re_outside_port_date_reminder_email_days * 1))
                outside_port_sched_pay_obj = sched_pay_obj.search(
                    [('purchase_order_id', '=', po_obj.id), ('payment_status', '=', 'unpaid'), ('action_type', '=', 'outside_port')])
                outside_port_sched_pay_obj.write({
                    'one_payment_method': vals[
                        'outside_port_one_payment_method'] if 'outside_port_one_payment_method' in vals else po_obj.outside_port_one_payment_method.id,
                    'action_date': vals['outside_port_date'] if 'outside_port_date' in vals else po_obj.outside_port_date,
                    'schedule_date': re_outside_port_date_deadline,
                    'action_percent': re_outside_port_percent,
                    'action_amount': ((po_obj.amount_total * re_outside_port_percent) / 100),
                })
                outside_port_sched_pay_obj.activity_id.action_done()
                po_outside_port_date_activity = po_obj.activity_schedule(
                    'purchase.po_outside_port_date',
                    summary=_("Outside Port Reminder"),
                    user_id=po_obj.user_id.id,
                    note='Outside Port Date : {} \n With payment : {}'.format(outside_port_sched_pay_obj.schedule_date,
                                                                              outside_port_sched_pay_obj.action_amount),
                    date_deadline=outside_port_sched_pay_obj.schedule_date,
                    activity_type_id=self.env.ref('one_silver_purchase.po_outside_port_date', raise_if_not_found=False).id
                )
                outside_port_sched_pay_obj.activity_id = po_outside_port_date_activity.id

    def do_one_payment(self):
        for record in self:
            record.payment_status = 'paid'
            record.activity_id.action_done()

    def de_one_unpaid(self):
        for record in self:
            record.payment_status = 'unpaid'
            record.activity_id.unlink()
            xml_type_id = ''
            title_str = ''
            if record.action_type == 'receipt':
                xml_type_id = 'po_receipt_date'
                title_str = 'Receipt'
            if record.action_type == 'shipping':
                xml_type_id = 'po_shipping_date'
                title_str = 'Shipping'
            if record.action_type == 'inside_port':
                xml_type_id = 'po_inside_port_date'
                title_str = 'Inside_port'
            if record.action_type == 'outside_port':
                xml_type_id = 'po_outside_port_date'
                title_str = 'Outside_port'
            if record.action_type == 'deadline':
                xml_type_id = 'po_deadline_date'
                title_str = 'Order Deadline'
            po_receipt_date_activity = record.purchase_order_id.activity_schedule(
                'purchase.{}'.format(xml_type_id),
                summary=_("{} Date Reminder".format(title_str)),
                user_id=record.purchase_order_id.user_id.id,
                note='{} Date : {} \n With payment : {}'.format(title_str, record.schedule_date, record.action_amount),
                date_deadline=record.schedule_date,
                activity_type_id=self.env.ref('one_silver_purchase.{}'.format(xml_type_id), raise_if_not_found=False).id
            )
            record.activity_id = po_receipt_date_activity.id


