
from odoo import models, fields


class ProductSaleHistoryWizard(models.TransientModel):
    _name = 'product.purchase.order.history'
    _rec_name = 'product_id'

    product_purchase_history = fields.One2many(comodel_name='product.purchase.history.line',
                                           inverse_name='order_line_id',
                                           string='Product Purchase Price History',
                                           help="shows the product purchase history of the vendor" , limit=5)
    product_id = fields.Many2one(comodel_name='product.product', string="Product:")


class SalesPriceHistory(models.TransientModel):
    _name = 'product.purchase.history.line'
    _rec_name = 'purchase_order_id'
    _order = "purchase_order_date desc"


    order_line_id = fields.Many2one(comodel_name='product.purchase.order.history')
    purchase_order_id = fields.Many2one(comodel_name='purchase.order', string="Purchase order")
    purchase_order_line_id = fields.Many2one(comodel_name='purchase.order.line', string="PO Line")
    purchase_order_date = fields.Datetime(string='Order Date', related='purchase_order_id.date_order')
    history_sequence = fields.Char(string='PO Seq.', related='purchase_order_id.one_sequence')
    history_currency = fields.Many2one(comodel_name='res.currency', related='purchase_order_id.currency_id')
    history_price = fields.Char(string='Unit Price')
    history_qty = fields.Float(string='Quantity')
    history_total = fields.Float(string='Total')
    history_uom = fields.Many2one(comodel_name='uom.uom', related='purchase_order_line_id.product_uom')
    history_uom_factor = fields.Float(string='Uom Factor', related='history_uom.factor')

    history_discount = fields.Float(string='Discount', related='purchase_order_line_id.discount')
