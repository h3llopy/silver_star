from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    def print_purchase_voucher_report(self):
        data = {
            'model_id':self.id,
        }
        return self.env['purchase.order'].report_action(self=self, data=data)

    def print_purchase_custom_order(self):
        data = {
            'model_id':self.id,
        }
        return self.env['purchase.order'].report_action(self=self, data=data)


