
from odoo import models, fields


class ProductSaleHistoryWizard(models.TransientModel):
    _name = 'product.sale.order.history'
    _rec_name = 'product_id'

    product_sale_history = fields.One2many(comodel_name='product.sale.history.line',
                                           inverse_name='order_line_id',
                                           string='Product Sale Price History',
                                           help="shows the product sale history of the customer" , limit=5)
    product_id = fields.Many2one(comodel_name='product.product', string="Product:")


class SalesPriceHistory(models.TransientModel):
    _name = 'product.sale.history.line'
    _rec_name = 'sale_order_id'
    _order = "sale_order_date desc"


    order_line_id = fields.Many2one(comodel_name='product.sale.order.history')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale order")
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="SO Line")
    sale_order_date = fields.Datetime(string='Order Date', related='sale_order_id.date_order')
    history_sequence = fields.Char(string='SO Seq.', related='sale_order_id.one_sequence')
    history_currency = fields.Many2one(comodel_name='res.currency', related='sale_order_id.pricelist_id.currency_id')
    history_qty = fields.Float(string='Quantity')
    history_price = fields.Char(string='Unit Price')
    history_uom = fields.Many2one(comodel_name='uom.uom', related='sale_order_line_id.product_uom')
    history_uom_factor = fields.Float(string='Uom Factor', related='history_uom.factor')
    history_discount = fields.Float(string='Discount', related='sale_order_line_id.discount')
    history_cost = fields.Float(string='Cost', related='sale_order_line_id.purchase_price')
    history_total = fields.Float(string='Total')
