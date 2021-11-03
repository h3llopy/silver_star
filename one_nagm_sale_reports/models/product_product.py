""" Initialize Product Product """

from odoo import models


class ProductProduct(models.Model):
    """
        Inherit Product Product:
         -
    """
    _inherit = 'product.product'

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
