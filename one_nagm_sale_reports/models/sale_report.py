# -*- coding: utf-8 -*-
""" Initialize Sale Report """

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    """
        Inherit Sale Order Line:
         -
    """
    _inherit = 'sale.order.line'

    total_amount = fields.Float(
        compute='_compute_total_amount',
        store=True
    )

    returned_deliver_qty = fields.Float(
        compute='_compute_returned_delivery_qty', store=True
    )
    total_returned_deliver = fields.Float(
        compute='_compute_total_returned_deliver', store=True
    )
    canceled_deliver_qty = fields.Float(
        compute='_compute_canceled_delivery_qty', store=True
    )
    total_canceled_deliver = fields.Float(
        compute='_compute_total_canceled_deliver', store=True
    )
    delivered_amount = fields.Float(
        compute='_compute_delivered_amount', store=True
    )
    total_qty_delivered = fields.Float(
        related='product_uom_qty', store=True
    )
    credit_note_qty = fields.Float(
        compute='_compute_credit_note_qty', store=True
    )
    total_credit_note = fields.Float(
        compute='_compute_total_credit_note', store=True
    )
    returned_invoice_qty = fields.Float(
        compute='_compute_returned_invoice_qty', store=True
    )
    total_returned_invoice = fields.Float(
        compute='_compute_total_returned_invoice', store=True
    )

    @api.depends('returned_invoice_qty', 'price_unit')
    def _compute_total_returned_invoice(self):
        """ Compute total_returned_invoice value """
        for rec in self:
            rec.total_returned_invoice = rec.returned_invoice_qty * rec.price_unit

    @api.depends('credit_note_qty', 'price_unit')
    def _compute_total_credit_note(self):
        """ Compute total_credit_note value """
        for rec in self:
            rec.total_credit_note = rec.credit_note_qty * rec.price_unit

    @api.depends('canceled_deliver_qty', 'price_unit')
    def _compute_total_canceled_deliver(self):
        """ Compute total_canceled_deliver value """
        for rec in self:
            rec.total_canceled_deliver = rec.canceled_deliver_qty * rec.price_unit

    @api.depends('returned_deliver_qty', 'price_unit')
    def _compute_total_returned_deliver(self):
        """ Compute total_returned_deliver value """
        for rec in self:
            rec.total_returned_deliver = rec.returned_deliver_qty * rec.price_unit

    @api.depends('invoice_lines', 'invoice_lines.move_id.state')
    def _compute_credit_note_qty(self):
        """ Compute credit_note_qty value """
        for rec in self:
            rec.credit_note_qty = sum(
                (rec.invoice_lines.filtered(
                    lambda r: r.move_id.move_type == 'out_refund')).mapped(
                    'quantity'))

    @api.depends('qty_to_invoice', 'invoice_lines')
    def _compute_returned_invoice_qty(self):
        """ Compute returned_invoice_qty value """
        for rec in self:
            if rec.invoice_lines and rec.qty_invoiced == 0:
                rec.returned_invoice_qty = rec.qty_to_invoice
            elif rec.qty_invoiced == rec.product_uom_qty:
                rec.returned_invoice_qty = 00
            elif rec.qty_invoiced < rec.product_uom_qty and rec.qty_invoiced != 00:
                rec.returned_invoice_qty = rec.qty_to_invoice
            rec.returned_invoice_qty -= rec.credit_note_qty

    @api.depends('qty_to_deliver', 'move_ids')
    def _compute_returned_delivery_qty(self):
        """ Compute returned_delivery_qty value """
        for rec in self:
            rec.returned_deliver_qty = sum(
                (rec.move_ids.filtered(lambda r: r.picking_id.returned == True and r.state=='done')).mapped(
                    'product_uom_qty'))

    @api.depends('move_ids', 'move_ids.state')
    def _compute_canceled_delivery_qty(self):
        """ Compute canceled_delivery_qty value """
        for rec in self:
            rec.canceled_deliver_qty = sum(
                (rec.move_ids.filtered(lambda r: r.state == 'cancel')).mapped(
                    'product_uom_qty'))

    @api.depends('qty_delivered')
    def _compute_delivered_amount(self):
        """ Compute delivered_amount value """
        for rec in self:
            rec.delivered_amount = rec.price_unit * rec.qty_delivered

    @api.depends('qty_delivered')
    def _compute_total_amount(self):
        """ Compute total_deliver value """
        for rec in self:
            rec.total_amount = rec.product_uom_qty * rec.price_unit


class SaleReport(models.Model):
    """
        Inherit Sale Report:
         -
    """
    _inherit = 'sale.report'

    returned_deliver_qty = fields.Float(readonly=True, compute_sudo=True,
                                        store=True
                                        )
    total_amount = fields.Float(
        string="Total With out Disc&Tax", readonly=True, compute_sudo=True,
        store=True
    )
    returned_invoice_qty = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    canceled_deliver_qty = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    delivered_amount = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    credit_note_qty = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    total_qty_delivered = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    total_returned_deliver = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    total_canceled_deliver = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    total_credit_note = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )
    total_returned_invoice = fields.Float(
        readonly=True, compute_sudo=True, store=True
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields[
            'returned_deliver_qty'] = ", l.returned_deliver_qty as returned_deliver_qty"
        groupby += ', l.returned_deliver_qty'
        fields['total_amount'] = ", l.total_amount as total_amount"
        groupby += ', l.total_amount'
        fields[
            'returned_invoice_qty'] = ", l.returned_invoice_qty as returned_invoice_qty"
        groupby += ', l.returned_invoice_qty'
        fields[
            'canceled_deliver_qty'] = ", l.canceled_deliver_qty as canceled_deliver_qty"
        groupby += ', l.canceled_deliver_qty'
        fields['delivered_amount'] = ", l.delivered_amount as delivered_amount"
        groupby += ', l.delivered_amount'
        fields['credit_note_qty'] = ", l.credit_note_qty as credit_note_qty"
        groupby += ', l.credit_note_qty'
        fields[
            'total_qty_delivered'] = ", l.total_qty_delivered as total_qty_delivered"
        groupby += ', l.total_qty_delivered'
        fields[
            'total_returned_deliver'] = ", l.total_returned_deliver as total_returned_deliver"
        groupby += ', l.total_returned_deliver'
        fields[
            'total_canceled_deliver'] = ", l.total_canceled_deliver as total_canceled_deliver"
        groupby += ', l.total_canceled_deliver'
        fields[
            'total_credit_note'] = ", l.total_credit_note as total_credit_note"
        groupby += ', l.total_credit_note'
        fields[
            'total_returned_invoice'] = ", l.total_returned_invoice as total_returned_invoice"
        groupby += ', l.total_returned_invoice'

        return super(SaleReport, self)._query(with_clause, fields, groupby,
                                              from_clause)
