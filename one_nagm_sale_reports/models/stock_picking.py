""" Initialize Stock Picking """

from odoo import _, fields, models


class StockPicking(models.Model):
    """
        Inherit Stock Picking:
         - 
    """
    _inherit = 'stock.picking'

    returned = fields.Boolean()

    def action_cancel(self):
        """ Override action_cancel """
        res = super(StockPicking, self).action_cancel()
        self.returned = False
        return res


class StockReturnPicking(models.TransientModel):
    """
        Inherit Stock Return Picking:
         -
    """
    _inherit = 'stock.return.picking'

    def create_returns(self):
        for wizard in self:
            new_picking_id, pick_type_id = wizard._create_returns()
            self.env['stock.picking'].browse(new_picking_id).write(
                {'returned': True})
        # Override the context to disable all the potential filters that could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'default_partner_id': self.picking_id.partner_id.id,
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_planning_issues': False,
            'search_default_available': False,
        })
        return {
            'name': _('Returned Picking'),
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }
