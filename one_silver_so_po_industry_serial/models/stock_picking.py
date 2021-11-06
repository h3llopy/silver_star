#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/


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
        for record in self:
            if record.sale_id:
                record.source_one_sequence = record.sale_id.one_sequence
            elif record.purchase_id:
                record.source_one_sequence = record.purchase_id.one_sequence
            else:
                record.source_one_sequence = False

class StockPickingReturn(models.TransientModel):
    _inherit = 'stock.return.picking'

    _sql_constraints = [
        ('_unique_one_sequence', 'unique (one_sequence)', "Sequence must be unique"),
    ]
    one_sequence = fields.Char(string='Sequence', readonly=True, store=True)
    source_one_sequence = fields.Char()

