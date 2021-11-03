#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

#
#

#
#

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    _sql_constraints = [
        ('_unique_one_sequence', 'unique (one_sequence)', "Sequence must be unique"),
    ]
    income_one_sequence = fields.Char(string='In Sequence', readonly=True, store=True)
    outgoing_one_sequence = fields.Char(string='Out Sequence', readonly=True, store=True)
    source_one_sequence = fields.Char(string='Source', compute='_compute_one_sequence')

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.picking_type_code == 'incoming':
            res.income_one_sequence = self.env['one.sequence'].next_one_sequence(used_for='stock_picking',
                                                                                 partner_id=res.partner_id,
                                                                                 stock_picking_code=res.picking_type_code)
        if res.picking_type_code == 'outgoing':
            res.outgoing_one_sequence = self.env['one.sequence'].next_one_sequence(used_for='stock_picking',
                                                                                   partner_id=res.partner_id,
                                                                                   stock_picking_code=res.picking_type_code)

        return res

    def _compute_one_sequence(self):
        if self.sale_id:
            self.source_one_sequence = self.sale_id.one_sequence
        if self.purchase_id:
            self.source_one_sequence = self.purchase_id.one_sequence
        else:
            self.source_one_sequence = False

class StockPickingReturn(models.TransientModel):
    _inherit = 'stock.return.picking'

    _sql_constraints = [
        ('_unique_one_sequence', 'unique (one_sequence)', "Sequence must be unique"),
    ]
    one_sequence = fields.Char(string='Sequence', readonly=True, store=True)
    source_one_sequence = fields.Char()

    #
    # @api.model
    # def create(self, vals):
    #     res = super(StockPickingReturn, self).create(vals)
    #
    #     res.one_sequence = self.env['one.sequence'].next_one_sequence(used_for='stock_picking',
    #                                                                   partner_id=res.partner_id,
    #                                                                   stock_picking_code=res.picking_type_code)
    #     if res.sale_id:
    #         res.source_one_sequence = res.sale_id.one_sequence
    #     if res.purchase_id:
    #         res.source_one_sequence = res.purchase_id.one_sequence
    #     return res
