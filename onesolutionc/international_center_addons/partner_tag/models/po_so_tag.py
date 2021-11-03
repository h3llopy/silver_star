from odoo import api, fields, models


class PoTag(models.Model):
    _inherit = 'purchase.order'

    tag_po_ids = fields.Many2many(comodel_name="res.partner.category",
                                  string="tag", readonly=True)

    @api.onchange('partner_id')
    def _onchange_tag_ids(self):
        print('in onchange')
        if self.partner_id:
            print('in')
            self.tag_po_ids = self.partner_id.category_id
            x = self.partner_id.category_id
            print(x)


class SoTag(models.Model):
    _inherit = 'sale.order'
    tag_so_ids = fields.Many2many(comodel_name="res.partner.category",
                                  string="tag", readonly=True)

    @api.onchange('partner_id')
    def _onchange_tag_so_ids(self):
        print('in onchange')
        if self.partner_id:
            print('in')
            self.tag_so_ids = self.partner_id.category_id
            x = self.partner_id.category_id
            print(x)
