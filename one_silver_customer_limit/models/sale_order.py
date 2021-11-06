# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_due = fields.Monetary(related='partner_id.amount_due', currency_field='company_currency_id')
    company_currency_id = fields.Many2one(string='Company Currency', readonly=True,
                                          related='company_id.currency_id')
    credit_check = fields.Boolean(related='partner_id.credit_check')
    credit_warning = fields.Monetary(related='partner_id.credit_warning')
    credit_blocking = fields.Monetary(related='partner_id.credit_blocking')
    credit_alert = fields.Boolean(default=False, compute='_onchange_credit_alert_block')

    days_check = fields.Boolean(related='partner_id.days_check')
    days_warning = fields.Integer(related='partner_id.days_warning')
    days_blocking = fields.Integer(related='partner_id.days_blocking')
    days_alert = fields.Boolean()
    alert_days = fields.Integer(compute='_compute_alert_days', store=False)

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _onchange_credit_alert_block(self):
        if self.credit_check:
            if self.amount_due >= self.credit_warning:
                self.credit_alert = True
            else:
                self.credit_alert = False
        else:
            self.credit_alert = False

        if self.days_check:
            if self.alert_days >= self.days_warning:
                self.days_alert = True
            else:
                self.days_alert = False
        else:
            self.days_alert = False

    @api.onchange('partner_id')
    def _compute_alert_days(self):
        if self.days_check:
            last_order = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id)], order='date_order desc', limit=1)
            self.alert_days = (fields.date.today() - last_order.date_order.date()).days
        else:
            self.alert_days = 0

    @api.depends('amount_total', 'tax_totals_json', 'amount_untaxed')
    @api.onchange('amount_total', 'tax_totals_json', 'amount_untaxed')
    def _onchange_amount_total(self):
        if self.credit_check:
            if (self.amount_total + self.amount_due) > self.credit_blocking:
                if not (self.env.is_admin() or self.env.user.has_group('one_silver_customer_limit.allow_pass_customer_limit')):
                    raise AccessDenied('Customer credit limit exceeded.')
        if self.days_check:
            if self.alert_days >= self.days_blocking:
                if not (self.env.is_admin() or self.env.user.has_group('one_silver_customer_limit.allow_pass_customer_limit')):
                    raise AccessDenied('Customer credit limit exceeded.')

    def action_confirm(self):
        if self.credit_check:
            existing_move = self.env['account.move'].search(
                [('partner_id', '=', self.partner_id.id), ('state', '=', 'posted')])
            if (self.amount_total + self.amount_due) >= self.credit_blocking:
                if not (self.env.is_admin() or self.env.user.has_group('one_silver_customer_limit.allow_pass_customer_limit')):
                    raise AccessDenied(_('Customer credit limit exceeded.'))
                else:
                    view_id = self.env.ref('one_silver_customer_limit.view_warning_wizard_form')
                    context = dict(self.env.context or {})
                    context['message'] = "Customer Blocking limit exceeded, Do You want to continue?"
                    context['default_sale_id'] = self.id
                    if not self._context.get('warning'):
                        return {
                            'name': 'Warning',
                            'type': 'ir.actions.act_window',
                            'view_mode': 'form',
                            'res_model': 'one.customer.limit.warning.wizard',
                            'view_id': view_id.id,
                            'target': 'new',
                            'context': context,
                        }
                    else:
                        return super(SaleOrder, self).action_confirm()
            else:
                return super(SaleOrder, self).action_confirm()

        else:
            return super(SaleOrder, self).action_confirm()
