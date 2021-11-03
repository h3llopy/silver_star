from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    number_times_print = fields.Char(string='number times print', default='0')

    count = fields.Integer(default=0)

    def print_report_edit_button(self):
        if self.count == 0:
            self.number_times_print = 1
            self.count += 1
        else:
            self.number_times_print = "Copy " + str(self.count)
            self.count += 1
        return self.env.ref(
            'sale.action_report_saleorder').report_action(self)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    numbers_of_times_print = fields.Char(string='number times print',
                                         default='0')
    counter = fields.Integer(default=0)

    number_of_times_print = fields.Char(string='number times print',
                                        default='0')
    counting = fields.Integer(default=0)

    def print_report_button(self):
        if self.counter == 0:
            self.numbers_of_times_print = 1
            self.counter += 1
        else:
            self.numbers_of_times_print = "Copy " + str(self.counter)
            self.counter += 1
        return self.env.ref(
            'purchase.action_report_purchase_order').report_action(self)

    def print_quotation(self):
        self.write({'state': "sent"})
        if self.counting == 0:
            self.number_of_times_print = 1
            self.counting += 1
        else:
            self.number_of_times_print = "Copy " + str(self.counting)
            self.counting += 1
        return self.env.ref(
            'purchase.report_purchase_quotation').report_action(self)
