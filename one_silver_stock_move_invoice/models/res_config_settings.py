
from odoo import fields, models


class Settings(models.TransientModel):
    _inherit = 'res.config.settings'
    customer_journal_id = fields.Many2one('account.journal', string='Customer Journal',
                                          config_parameter='stock_move_invoice.customer_journal_id')
    vendor_journal_id = fields.Many2one('account.journal', string='Vendor Journal',
                                        config_parameter='stock_move_invoice.vendor_journal_id')
