from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean('is Agent', default=False)
    related_agent_user = fields.Many2one(comodel_name='res.users', string='Related Agent')

    def create_agent_user(self):
        for record in self:
            if record.is_agent:
                new_user =record.env['res.users'].create({
                    'name': record.name,
                    'partner_id': record.id,
                    'login': 'agent%s'%record.id,
                    'groups_id': [(6, 0, [self.env.ref('one_silver_customer_target.agent_user').id])],
                    'is_agent' : True

                })
                record.related_agent_user = new_user.id

    # user_id = fields.Many2one('res.users', string='Salesperson',
    #                       help='The internal user in charge of this contact.')
    # team_id = fields.Many2one(
    #     'crm.team', 'Sales Team',
    #     help='If set, this Sales Team will be used for sales and assignments related to this partner')
    #

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

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=2, default=_get_default_user)
    team_id = fields.Many2one(
            'crm.team', 'Sales Team', default=_get_default_team2, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.depends('crm_team_id')
    @api.onchange('team_id')
    def _on_change_team_id(self):
        members_of_team = self.env['crm.team.member'].search([('crm_team_id', '=', self.team_id.id)])
        return {'domain': {'user_id': [('id', 'in', members_of_team.user_id.ids)]}}

    @api.depends('user_id')
    @api.onchange('user_id')
    def _user_id_domain(self):
        in_team_ids = self.env['crm.team.member'].search([('crm_team_id', '=', self.team_id.id)])
        in_group_ids = self.env['res.users'].search(
            [('groups_id', 'in', self.env.ref('one_silver_customer_target.agent_user').id), ('id', 'not in', in_team_ids.user_id.ids)])
        return {'domain': {'user_id': [('id', 'in', in_group_ids.ids)]}}

    def get_customer_targets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Target',
            'view_mode': 'tree',
            'res_model': 'one.customer.target.result',
            'domain': [('customer_id', '=', self.id)],
            'context': "{'create': False}"
        }
