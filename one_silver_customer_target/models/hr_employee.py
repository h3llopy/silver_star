""" Initialize Hr Employee """

from odoo import fields, models


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    is_manager = fields.Boolean(related='job_id.is_manager')



class HrJob(models.Model):
    """
        Inherit Hr Job:
         -
    """
    _inherit = 'hr.job'

    is_manager = fields.Boolean(string='Is a Manager')
