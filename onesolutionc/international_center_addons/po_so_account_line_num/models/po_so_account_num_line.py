from odoo import api, fields, models


class Pnumline(models.Model):
    _inherit = 'purchase.order'
    count_line_po = fields.Integer(string="num of Products",
                                   compute='_compute_po_order_line',
                                   required=False, )

    @api.depends('order_line')
    def _compute_po_order_line(self):
        self.count_line_po = 0
        for s in self:
            for x in self.order_line:
                if x.product_id:
                    self.count_line_po += 1


class Sonumline(models.Model):
    _inherit = 'sale.order'
    count_line_so = fields.Integer(string="num of Products",
                                   compute='_compute_sale_order_line',
                                   required=False, )

    @api.depends('order_line')
    def _compute_sale_order_line(self):
        self.count_line_so = 0
        for s in self:
            for x in self.order_line:
                if x.product_id:
                    self.count_line_so += 1


class accountnumline(models.Model):
    _inherit = 'account.move'
    count_line_am = fields.Integer(string="num of Products",
                                   compute='_compute_account_invoice',
                                   required=False, )

    @api.depends('invoice_line_ids')
    def _compute_account_invoice(self):
        self.count_line_am = 0
        for s in self:
            for x in self.invoice_line_ids:
                if x.product_id:
                    self.count_line_am += 1
