#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / res_partner.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allow_custom_product = fields.Boolean(string='Allow Custom Products', default=False)
    products_count = fields.Integer(compute='_products_count')

    def _products_count(self):
        for record in self:
            record.products_count = self.env['product.customerinfo'].search_count([('name', '=', record.id)])

    def get_customer_custom_products(self):
        self.ensure_one()
        customer_products = self.env['product.customerinfo'].search([('name', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'view_mode': 'tree',
            'res_model': 'product.customerinfo',
            'domain': [('id', 'in', customer_products.ids)],
            'context': "{'create': False, 'from_customer':True}"
        }

    def action_add_customers_wizard(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Add Products'),
                'res_model': 'one.custom.product.partner.wizard',
                'target': 'new',
                'view_id': self.env.ref('one_silver_custom_product.add_products_to_customer').id,
                'view_mode': 'form',
                'context': "{'partner_id':%s}" % self.id
                }


class PartnerProductsWizard(models.TransientModel):
    _name = 'one.custom.product.partner.wizard'

    @api.depends('product_ids')
    def _get_customer_selected_products(self):
        products_ids = self.env['product.customerinfo'].search([('name', '=', self.env.context.get('default_partner_id'))]).product_id.product_tmpl_id.ids
        return [('allow_customer', '=', True), ('id', 'not in', products_ids)]

    partner_id = fields.Many2one(comodel_name='res.partner')
    product_ids = fields.Many2many(comodel_name='product.template', string='Products', relation='product_tmpl_partner_rel',
                                   domain=_get_customer_selected_products)

    def add_custom_products(self):
        if self.product_ids:
            for line in self.product_ids:
                self.env['product.customerinfo'].create({
                    'name': self.env.context['active_id'],
                    'product_name': line.name,
                    'product_code': line.name,
                    'sequence': 0,
                    'product_uom': line.uom_id.id,
                    'min_qty': 0,
                    'price': line.list_price,
                    'company_id': line.company_id.id,
                    'currency_id': line.currency_id.id,
                    'date_start': False,
                    'date_end': False,
                    'product_id': line.product_variant_id.id,
                    'product_variant_count': line.product_variant_count,
                    'delay': 0,
                })
