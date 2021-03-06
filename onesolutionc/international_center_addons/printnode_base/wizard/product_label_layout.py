# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    picking_quantity = fields.Selection(
        selection_add=[('custom_per_product', 'Custom Per Product')],
        ondelete={'custom_per_product': 'set default'}
    )

    printer_id = fields.Many2one(
        comodel_name='printnode.printer',
        default=lambda self: self.env.user.printnode_printer.id,
    )

    printer_bin = fields.Many2one(
        'printnode.printer.bin',
        string='Printer Bin',
        required=False,
        domain='[("printer_id", "=", printer_id)]',
    )
    product_line_ids = fields.One2many(
        comodel_name='product.label.layout.line',
        inverse_name='wizard_id',
        string='Products',
    )
    product_tmpl_line_ids = fields.One2many(
        comodel_name='product.label.layout.line',
        inverse_name='wizard_id',
        string='Products (Templates)',
    )

    active_model = fields.Char(
        string='Active Model'
    )

    status = fields.Char(
        related='printer_id.status',
    )

    def _get_printers_from_preferences(self):
        from_user = self.env.user.printnode_printer
        from_company = self.env.company.printnode_printer
        return from_user, from_company

    def _get_allowed_printers(self):
        from_user_rules = self.env['printnode.rule'].search([
            ('user_id', '=', self.env.uid),
            ('report_id.model', '=', 'product.product'),
        ]).mapped('printer_id')
        from_user, from_company = self._get_printers_from_preferences()
        return list(set(sum((from_user_rules.ids, from_user.ids, from_company.ids), [])))

    @api.model
    def default_get(self, fields_list):
        default_vals = super(ProductLabelLayout, self).default_get(fields_list)
        available_printers = self._get_allowed_printers()
        if len(available_printers) == 1:
            default_vals['printer_id'] = available_printers.pop()

        move_line_ids = self.env.context.get('default_move_line_ids')
        if default_vals.get('picking_quantity') == 'picking':
            default_vals['active_model'] = 'product.product'
            qties = defaultdict(
                int,
                {k: 0 for k in self.env.context.get('default_product_ids', [])}
            )
            if move_line_ids:
                uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)
                for line in self.env['stock.move.line'].browse(move_line_ids):
                    if line.product_uom_id.category_id == uom_unit:
                        qties[line.product_id.id] += line.qty_done
            default_vals['product_line_ids'] = [(0, 0, {
                'product_id': p,
                'quantity': int(q)
            }) for p, q in qties.items()]
        elif self.env.context.get('default_product_tmpl_ids'):
            default_vals['active_model'] = 'product.template'
            default_vals['product_tmpl_line_ids'] = [(0, 0, {
                'product_tmpl_id': p_id,
                'quantity': 1
            }) for p_id in self.env.context.get('default_product_tmpl_ids')]
        else:
            default_vals['active_model'] = 'product.product'
            default_vals['product_line_ids'] = [(0, 0, {
                'product_id': p_id,
                'quantity': 1
            }) for p_id in self.env.context.get('default_product_ids', [])]

        return default_vals

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if self.picking_quantity != 'custom_per_product':
            return xml_id, data
        if self.active_model == 'product.template' and self.product_tmpl_line_ids:
            data['quantity_by_product'] = {
                line.product_tmpl_id.id: line.quantity for line in self.product_tmpl_line_ids
            }
        elif self.active_model == 'product.product' and self.product_line_ids:
            data['quantity_by_product'] = {
                line.product_id.id: line.quantity for line in self.product_line_ids
            }
        return xml_id, data

    def _check_quantity(self):
        for rec in self.product_line_ids:
            if rec.quantity < 1:
                raise ValidationError(
                    _(
                        'Quantity can not be less than 1 for product {product}'
                    ).format(**{
                        'product': rec.product_id.display_name or rec.product_tmpl_id.display_name,
                    })
                )

    def process(self):
        self.ensure_one()

        if self.picking_quantity == 'custom_per_product':
            self._check_quantity()

        # if no printer than download PDF
        if not self.printer_id:
            return super(ProductLabelLayout, self.with_context(download_only=True)).process()

        xml_id, data = self._prepare_report_data()

        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))

        return self.env.ref(xml_id).with_context(
            printer_id=self.printer_id.id,
            printer_bin=self.printer_bin.id
        ).report_action(None, data=data)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super().fields_get(allfields=allfields, attributes=attributes)
        if 'picking_quantity' in fields:
            if self.env.context.get('default_picking_quantity') != 'picking':
                fields['picking_quantity'].update({
                    'selection': [
                        ('custom', 'Custom'),
                        ('custom_per_product', 'Custom Per Product')
                    ]
                })
        return fields


class ProductLabelLayoutLine(models.TransientModel):
    _name = 'product.label.layout.line'
    _description = 'Choose the sheet layout to print the labels / Line'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product (Template)',
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )

    quantity = fields.Integer(
        required=True,
        default=1,
    )

    wizard_id = fields.Many2one(
        comodel_name='product.label.layout',
    )
