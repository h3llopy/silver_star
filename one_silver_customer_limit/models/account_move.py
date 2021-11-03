#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / account_move.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from datetime import datetime

from odoo import models, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

