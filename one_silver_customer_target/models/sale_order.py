from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_have_target = fields.Boolean(default=False)


    @api.model
    def _get_default_user(self):
        in_team = self.env['crm.team.member'].search([('user_id', '=', self.env.uid)]).crm_team_id.ids
        if in_team:
            return self.env.uid
        else:
            return False

    @api.model
    def _get_default_team2(self):
        in_teams = self.env['crm.team.member'].search([('user_id', '=', self.env.uid)]).crm_team_id.ids
        if in_teams:
            return in_teams[0]
        else:
            return False

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=2, default=_get_default_user, domain=lambda self:['|', ('id', 'in', self.env['crm.team.member'].search([]).user_id.ids), ('share', '=', False)], )
    team_id = fields.Many2one(
        'crm.team', 'Sales Team', default=_get_default_team2, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.depends( 'user_id')
    @api.onchange( 'user_id')
    def _on_change_team_id(self):
        for record in self:
            members_of_team = self.env['crm.team.member'].search([])
            return {'domain': {'user_id': ['|', ('id', 'in', members_of_team.user_id.ids), ('share', '=', False)]}}

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.uid
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        values['team_id'] = self.partner_id.team_id.id
        self.update(values)


        current_target = self.env['one.customer.target'].search(
            [('customer_id', '=', self.partner_id.id), ('start_date', '<=', self.date_order.date()),
             ('end_date', '>=', self.date_order.date())])
        self.partner_have_target = True if current_target else False

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
            self.team_id = self.team_id.id



class SealOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remian_target_qty = fields.Float(string='Rem.Target qty', readonly=True, store=True)

    @api.onchange('product_id', 'product_uom')
    def _onchange_compute_remain_target(self):
        current_target = self.env['one.customer.target'].search(
            [('customer_id', '=', self.order_id.partner_id.id), ('start_date', '<=', self.order_id.date_order.date()),
             ('end_date', '>=', self.order_id.date_order.date())])
        current_target_line = current_target.line_ids.search(
            [('target_id', '=', current_target.id), ('product_id', '=', self.product_id.id),('product_uom', '=', self.product_uom.id)], limit=1)
        self.remian_target_qty = current_target_line.sold_qty - current_target_line.return_qty