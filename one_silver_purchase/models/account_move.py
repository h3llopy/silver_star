#  One Solution
#
#  @author :ibralsmn.
#  @mailto : ibralsmn@onesolutionc.com.
#  @company : onesolutionc.com.
#  @project : international_center.
#  @module:  addons.
#  @file : account_move.py.
#  @created : 10/6/21, 9:40 AM.
#
import datetime

from odoo import models, api, _, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _purchase_orders_domain(self):
        landed_costs = self.env['stock.landed.cost'].search([('vendor_bill_id','!=',self.id)]).mapped('picking_ids').purchase_id.ids
        return [('id','not in', landed_costs)]

    vendor_ref_date = fields.Date(string='Bill Reference Date')
    land_cost_purchase_order_ids = fields.Many2many(comodel_name='purchase.order', relation='land_cost_purchase_order_rel', domain=_purchase_orders_domain)
    is_have_land_costs = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMove, self).create(vals_list)
        for record in res:
            if record.is_have_land_costs:
                no_landed_cost_activity = record.activity_schedule(
                    'one_silver_purchase.invoice_without_landed_cost',
                    summary=_("No Landed Cost"),
                    user_id=record.user_id.id,
                    note='Invoice Created Without Landed Cost',
                    date_deadline=datetime.datetime.now(),
                    activity_type_id=self.env.ref('one_silver_purchase.invoice_without_landed_cost', raise_if_not_found=False).id
                )
        return res

    @api.depends('invoice_line_ids')
    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_land_costs(self):
        landed_list = []
        for line in self.invoice_line_ids:
            if line.is_landed_costs_line:
                landed_list.append(line.id)
        if landed_list:
            self.is_have_land_costs = True
        else:
            self.is_have_land_costs = False


    def button_create_landed_costs(self):
        for activity in self.activity_ids:
            if activity.display_name == 'No Landed Cost' and activity.res_model == 'account.move':
                activity.action_done()
        return super().button_create_landed_costs()


