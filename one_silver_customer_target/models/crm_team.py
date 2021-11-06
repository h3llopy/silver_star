from odoo import models, fields, api


class CrmTeam(models.Model):
    _inherit = "crm.team"

    member_ids = fields.One2many(comodel_name='crm.team.member', inverse_name='crm_team_id', string='Channel Members')

    manager_id = fields.Many2one(comodel_name='hr.employee', )

    def _default_manger_id(self):
        """ Set Manager """
        for rec in self:
            if rec.user_id:
                if not self.manager_id:
                    employee_id = self.env['hr.employee'].search(
                        [('user_id', '=', rec.user_id.id)])
                    if employee_id and employee_id.job_id and \
                            employee_id.job_id.department_id and \
                            employee_id.job_id.department_id.manager_id:
                        rec.manager_id = employee_id.job_id.department_id.manager_id.id
                    else:
                        rec.manager_id = False
                else:
                    rec.manager_id = False


class CrmTeamMember(models.Model):
    _inherit = 'crm.team.member'

    user_target = fields.Float(string='Target')
    partner_id = fields.Many2one(related='user_id.partner_id', )
    company_id = fields.Many2one(related='partner_id.company_id', )
    name = fields.Char(related='partner_id.name', )
    share = fields.Boolean(default=False, compute_sudo=True, string='Share User', store=True,
                           help="External user with limited access, created only for the purpose of sharing data.")


    @api.depends('user_id')
    @api.onchange('user_id')
    def _user_id_domain(self):
        in_group_ids = self.env['res.users'].search(
            ['|',('groups_id', 'in', self.env.ref('one_silver_customer_target.agent_user').id), ('share','=',False)])
        if self.crm_team_id:
            return {'domain': {'user_id': [('id','!=', self.crm_team_id.user_id.id),('id', 'in', in_group_ids.ids), ('id', 'in', self.user_in_teams_ids.ids), ('company_ids', 'in', self.user_company_ids.ids)]}}
        else:
            return {'domain': {'user_id': [('id', 'in', in_group_ids.ids), ('id', 'in', self.user_in_teams_ids.ids), ('company_ids', 'in', self.user_company_ids.ids)]}}


