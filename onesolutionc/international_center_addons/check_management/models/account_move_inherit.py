# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    check_id = fields.Many2one(comodel_name='check.payment.transaction',
                               string='Check')


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    check_id = fields.Many2one(comodel_name='check.payment.transaction',
                               ondelete='cascade', string='Check')
