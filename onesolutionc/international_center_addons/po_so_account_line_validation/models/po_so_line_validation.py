from odoo import _, api, models


# LOGGER = logging.getLogger(_name_)
class pvalid(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def onchange_po_order_line(self):
        list_line_po_ids = []

        for x in self.order_id.order_line:
            if x.id.origin or x.id.ref:

                for s in list_line_po_ids:

                    if self.product_id.id == s.product_id.id:
                        return {'warning': {'title': _("Warning"),
                                            'message': "The product has already been added"}}

                list_line_po_ids.append(x)


#
class Sovalid(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def onchange_o_order_line(self):
        list_line_so_ids = []

        for x in self.order_id.order_line:
            if x.id.origin or x.id.ref:

                for s in list_line_so_ids:

                    if self.product_id.id == s.product_id.id:
                        return {'warning': {'title': _("Warning"),
                                            'message': "The product has already been added"}}

                list_line_so_ids.append(x)


class accountvalid(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def onchange_ac_order_line(self):
        list_line_ac_ids = []

        for x in self.move_id.invoice_line_ids:
            if x.id.origin or x.id.ref:

                for s in list_line_ac_ids:

                    if self.product_id.id == s.product_id.id:
                        return {'warning': {'title': _("Warning"),
                                            'message': "The product has already been added"}}

                list_line_ac_ids.append(x)
