from odoo import models, fields


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    list_price = fields.Float(string='Standard Price',  readonly=True)
    min_lst_price = fields.Float(string='Min Price' , readonly=True)
    price_unit = fields.Float(string='Price' , readonly=True)
    amount_total = fields.Float(string='Order Total', readonly=True)
    product_uomm = fields.Many2one(comodel_name='uom.uom', string='Unitt', readonly=True)
    unit_ratio = fields.Float(string='Unit Rito', readonly=True )
    expire_date = fields.Date()
    prod_expire_date = fields.Date()
    unit_lc_cost = fields.Float( )

    def _select(self):
        res = super()._select()
        res += ", (CASE WHEN t.list_price IS NOT NULL THEN t.list_price ELSE 0.0 END) AS list_price"
        res += ", (CASE WHEN t.min_list_price IS NOT NULL THEN t.min_list_price ELSE 0.0 END) AS min_lst_price"
        res += ", (CASE WHEN l.price_unit IS NOT NULL THEN l.price_unit ELSE 0.0 END) AS price_unit"
        res += ", (CASE WHEN po.amount_total IS NOT NULL THEN po.amount_total ELSE 0.0 END) AS amount_total"
        res += ", (CASE WHEN l.unit_ratio IS NOT NULL THEN l.unit_ratio ELSE 0.0 END) AS unit_ratio"
        res += ", (CASE WHEN l.unit_lc_cost IS NOT NULL THEN l.unit_lc_cost ELSE 0.0 END) AS unit_lc_cost"
        # res += ", (CASE WHEN sum(p.weight * l.product_qty/line_uom.factor*product_uom.factor) IS NOT NULL THEN sum(p.weight * l.product_qty/line_uom.factor*product_uom.factor) ELSE 0.0 END) AS weight"
        # res += ", (CASE WHEN sum(p.volume * l.product_qty/line_uom.factor*product_uom.factor) IS NOT NULL THEN sum(p.volume * l.product_qty/line_uom.factor*product_uom.factor) ELSE 0.0 END) AS volume"
        res += ", l.product_uom AS product_uomm"
        res += ", l.expire_date AS expire_date"
        res += ", l.prod_expire_date AS prod_expire_date"
        return res

    def _group_by(self):
        return super()._group_by() + ",t.list_price, min_lst_price, price_unit,amount_total, unit_ratio,product_uomm,unit_lc_cost,expire_date,prod_expire_date"

