""" Initialize Product Template """

from odoo import models, fields


class ProductTemplate(models.Model):
    """
        Inherit Product Template:
         - 
    """
    _inherit = 'product.template'

    seller_id = fields.Many2many(comodel_name='res.partner', string='Vendor',compute="_compute_saller_id")
    tags_ids = fields.Many2many(comodel_name='res.partner.category', string='Tags'
                                )
    country_id = fields.Many2one(comodel_name='res.country', string='country')
    weather_digit = fields.Float(string='Weather')

    def _compute_saller_id(self):
        for record in self:
            record.seller_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', record.id)], order='sequence asc').name.ids


    def get_vendor_product_code(self):
        """ Get Vendor Product Code """
        seller_id = self.env['product.supplierinfo'].search(
            [('id', 'in', self.seller_ids.ids)], order='sequence asc', limit=1)
        if seller_id:
            return seller_id.product_code

    def get_vendor_product_price(self):
        """ Get Vendor Product Price """
        seller_id = self.env['product.supplierinfo'].search(
            [('id', 'in', self.seller_ids.ids)], order='sequence asc', limit=1)
        if seller_id:
            return seller_id.price
