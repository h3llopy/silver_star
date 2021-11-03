#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / pricelist.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

from odoo import models, fields


class PriceList(models.Model):
    _inherit = 'product.pricelist'

    employee_ids = fields.One2many(comodel_name='one.product.pricelist.employee', string='Employee\'s',
                                   inverse_name='pricelist_id')


class PriceListEmployee(models.Model):
    _name = 'one.product.pricelist.employee'

    user_id = fields.Many2one(comodel_name='res.users', string='Employee', index=True, tracking=True,
                              required=True, domain=lambda self: self._get_user_limit())
    partner_id = fields.Many2one(comodel_name='res.partner', related='user_id.partner_id', string='Employee',
                                 store=True)
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', store=True)

    increase_percent = fields.Float(string='Increase %')
    increase_amount = fields.Float(string='Increase $')
    decrease_percent = fields.Float(string='Decrease %')
    decrease_amount = fields.Float(string='Decrease $')
    active = fields.Boolean(string='Active', default=True)

    def _get_user_limit(self):
        allowed_employees = self.env['res.users'].search([('user_limit_type', 'in', ['user_limit'])]).ids

        return "[('id','in', %s )]" % allowed_employees


class PriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    price_unit_min = fields.Monetary(string='Min Unit Price', default=0.0)
    price_min = fields.Monetary(string='Min Price', compute='_get_pricelist_item_min_price', )

    def _get_pricelist_item_min_price(self):
        for item in self:
            item.price_min = item.price_unit_min

    def get_min_price(self, line):
        selection_dict = dict()
        for item in self:
            if (line.product_template_id.categ_id == item.categ_id) and line.product_template_id.categ_id and item.applied_on == '2_product_category':
                selection_dict.update({'4': item.price_min})
            elif (line.product_template_id == item.product_tmpl_id) and line.product_template_id and item.applied_on == '1_product':
                selection_dict.update({'3': item.price_min})
            elif (line.product_id == item.product_id) and line.product_id and item.applied_on == '0_product_variant':
                selection_dict.update({'2': item.price_min})
            elif item.applied_on == '3_global':
                selection_dict.update({'5': item.price_min})
            else:
                selection_dict.update({'1': line.product_template_id.min_list_price})
        sorted_selection_dict = dict(sorted(selection_dict.items()))
        if selection_dict:
            return (sorted_selection_dict[next(iter(sorted_selection_dict))])
