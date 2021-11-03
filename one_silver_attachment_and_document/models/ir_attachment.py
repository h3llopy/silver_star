""" Initialize Ir Attachment """

from odoo import api, fields, models


class IrAttachment(models.Model):
    """
        Inherit Ir Attachment:
         -
    """
    _inherit = 'ir.attachment'

    select_model = fields.Selection(
        [('sale', 'Sale'),
         ('purchase', 'Purchase')],
    )

    sale_id = fields.Many2one(
        'sale.order', string='Sale Order'
    )
    purchase_id = fields.Many2one(
        'purchase.order', string='PO'
    )

    @api.onchange('sale_id')
    def _onchange_sale_id(self):
        """ sale_id """
        if self.sale_id:
            self.res_id = self.sale_id.id

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        """ purchase_id """
        if self.purchase_id:
            self.res_id = self.purchase_id.id

    @api.model
    def create(self, vals_list):
        """ Override create """
        # vals_list ={'field': value}  -> dectionary contains only new filled fields
        res = super(IrAttachment, self).create(vals_list)
        if res.select_model == 'sale':
            res.write({'res_model': 'sale.order',
                       'res_id': res.sale_id.id})
        elif res.select_model == 'purchase':
            res.write({'res_model': 'purchase.order',
                       'res_id': res.purchase_id.id})
        return res

    def write(self, vals):
        res = super(IrAttachment, self).write(vals)
        for rec in self:
            if 'sale_id' in vals:
                rec.write({'res_model': 'sale.order',
                           'res_id': rec.sale_id.id})
            elif 'purchase_id' in vals:
                rec.write({'res_model': 'purchase.order',
                           'res_id': rec.purchase_id.id})
        return res
