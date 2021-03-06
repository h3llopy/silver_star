# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields

SECURITY_GROUP = 'printnode_base.printnode_security_group_user'


class PrintNodeScenarioMixin(models.AbstractModel):
    _name = 'printnode.scenario.mixin'
    _description = 'Abstract scenario printing mixin'

    printnode_printed = fields.Boolean(default=False)

    def print_scenarios(self, action, ids_list=None, **kwargs):
        """
        Find all scenarios for current model and print reports.

        Returns True when something printed or False in other cases.
        """
        return self.env['printnode.scenario'].print_reports(
            action=action,
            ids_list=ids_list or self.mapped('id'),
            **kwargs)
