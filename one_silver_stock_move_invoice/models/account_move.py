from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def _onchange_picking_id(self):
        picking_ids = self.env['stock.picking'].search([('partner_id', '=', self.partner_id.id)])
        return {'domain': {'picking_id': [('id', 'in', picking_ids.ids)]}}

    picking_id = fields.Many2one('stock.picking', string='Picking', )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends('product_id', 'product_tmpl_id')
    @api.onchange('product_id', 'product_tmpl_id')
    def get_customer_domain(self):
        list_ids = []
        customer_allowed_products = self.env['product.customerinfo'].search([('name', '=', self.partner_id.id)])
        if customer_allowed_products:
            if self.partner_id.allow_custom_product:
                return {'domain': {

                    'product_id': ['|',('id', 'in', customer_allowed_products.mapped('product_id').ids),('landed_cost_ok','=',True)],
                    'product_tmpl_id': ['|',
                        ('id', 'in', customer_allowed_products.mapped('product_tmpl_id').ids),('landed_cost_ok','=',True)]
                }}
