#  One Solution
#
#  @author :ibralsmn.
#  @mailto : ibralsmn@onesolutionc.com.
#  @company : onesolutionc.com.
#  @project : international_center.
#  @module:  addons.
#  @file : customer_inventory.py.
#  @created : 10/10/21, 6:38 AM.
#
import datetime

from odoo import fields, models, api


class CustomerInventory(models.Model):
    _name = 'one.customer.inventory'
    _rec_name = 'product_id'
    company_id = fields.Many2one(string="Company", comodel_name='res.company', default=lambda self: self.env.company.id)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    product_tmpl_id = fields.Many2one(comodel_name='product.template', related='product_id.product_tmpl_id', store=True, string='Product Template')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', index=True, ondelete='cascade', required=True, domain="[('product_tmpl_id','=', product_tmpl_id)]")
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial',domain="[('product_id','=', product_id), ('company_id', '=', company_id)]", check_company=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure', required=True, domain="[('category_id', '=', product_uom_category_id)]")
    balance = fields.Float(string='Balance', store=True, readonly=True)
    move_type = fields.Selection(selection=[('sale', 'Sales'), ('return', 'Return'), ('reading', 'Reading')], string='Move Type')
    inv_qty = fields.Float(string='Quantity')
    stock_move_id = fields.Many2one(comodel_name='stock.picking', string='Stock Move')
    move_date = fields.Date(string='Move Date', default=fields.datetime.now())

    def calculate_qty(self, move_type, move_qty, customer_id, product_id, uom_id,stock_move=None, inventory_date=None):
        if move_type in ['sale', 'return']:
            inventory_ids = self.env['one.customer.inventory'].search([('customer_id', '=', customer_id.id), ('product_id', '=', product_id.id), ('product_uom_id', '=', uom_id.id)], order="move_date asc")
            new_inventory_id = self.env['one.customer.inventory'].with_context(readin_inv=True).create({
                'customer_id': customer_id.id,
                'product_id': product_id.id,
                'product_tmpl_id': product_id.product_tmpl_id.id,
                'product_uom_id': uom_id.id,
                'move_type': move_type,
                'inv_qty': move_qty,
                'stock_move_id': stock_move.id if stock_move else False,
                'move_date': stock_move.date if stock_move else inventory_date if inventory_date else datetime.datetime.now(),
                'balance': (
                    (inventory_ids[0].balance + move_qty) if move_type == 'sale' else ((inventory_ids[0].balance - move_qty) * -1) if move_type == 'return' else move_qty) if inventory_ids else move_qty
            })
    @api.model
    def create(self, vals_list):
        inventory_ids = self.env['one.customer.inventory'].search([('customer_id', '=', vals_list['customer_id']), ('product_id', '=', vals_list['product_id']), ('product_uom_id', '=', vals_list['product_uom_id'])], order="move_date asc")
        vals_list['balance']= ((inventory_ids[0].balance + vals_list['inv_qty']) if vals_list['move_type'] == 'sale' else ((inventory_ids[0].balance - vals_list['inv_qty']) * -1) if vals_list['move_type'] == 'return' else vals_list['inv_qty']) if inventory_ids else vals_list['inv_qty']
        return super(CustomerInventory, self).create(vals_list)
