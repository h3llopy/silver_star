#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / res_partner.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError, Warning


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allow_free_product = fields.Boolean(string='Allow Free Products')
    free_types_allowed = fields.One2many(comodel_name='one.free.type.customer', string='Allowed Free Types', inverse_name='customer_id')

    @api.depends('free_types_allowed')
    @api.onchange('free_types_allowed')
    def _onchange_free_types_allowed(self):
        list_ids = []
        if self.free_types_allowed:
            for line in self.free_types_allowed:
                if line.free_type_id.id in list_ids:
                    raise ValidationError('Free type must be unique')
                else:
                    list_ids.append(line.free_type_id.id)
        else:
            pass
