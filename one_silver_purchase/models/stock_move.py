import datetime

from odoo import models, api, fields


class Picking(models.Model):
    _inherit = "stock.picking"



class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    production_exp_date = fields.Datetime(string='Production Date', required=True, default=datetime.datetime.now())
    expiration_date = fields.Datetime(string='Expiration Date', compute='_compute_expiration_date', store=True,
                                      help='This is the date on which the goods with this Serial Number may'
                                           ' become dangerous and must not be consumed.')

    @api.depends('product_id', 'picking_type_use_create_lots', 'production_exp_date')
    @api.onchange('production_exp_date')
    def _compute_expiration_date(self):
        for move_line in self:
            if move_line.picking_type_use_create_lots:
                if move_line.product_id.use_expiration_date:
                    move_line.expiration_date = move_line.production_exp_date + datetime.timedelta(days=move_line.product_id.expiration_time)
                else:
                    move_line.expiration_date = False
