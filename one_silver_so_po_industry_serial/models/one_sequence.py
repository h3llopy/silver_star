#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

import logging
from datetime import date, datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class OneSequence(models.Model):
    _name = 'one.sequence'
    _description = 'Sequence'
    _order = 'name'
    _sql_constraints = [
        ('_unique_prefix', 'unique (prefix,number_next)', "Prefix must be unique"),
    ]
    name = fields.Char(required=True)
    code = fields.Char(string='Sequence Code')
    used_for = fields.Selection(
        selection=[('stock_picking', 'Stock Picking'), ('sale', 'Sale Order'), ('purchase', 'Purchase Order')],
        string='Used For', required=True)
    use_level = fields.Selection(selection=[('industry', 'Industry'), ('category', 'Category'), ('partner', 'Partner')],
                                 required=True)
    stock_picking_code = fields.Selection(selection=[('incoming', 'Receipt'), ('outgoing', 'Delivery')],
                                          string='Type of Operation')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', domain=[('parent_id', '=', False)],
                                 check_company=True, copy=False, ondelete='restrict', )
    industry_id = fields.Many2one(comodel_name='res.partner.industry', string='Industry', copy=False,
                                  ondelete='restrict')
    category_id = fields.Many2one(comodel_name='one.partner.category', string='Category', copy=False,
                                  ondelete='restrict')
    stock_picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string='Stock Operations Types',
                                            check_company=True, copy=False, ondelete='restrict')
    active = fields.Boolean(default=True)
    prefix = fields.Char(help="Prefix value of the record for the sequence", trim=False, compute='_get_sequence_prefix',
                         store=True)
    number_increment = fields.Integer(string='Step', required=True, default=1)
    padding = fields.Integer(string='Sequence Size', required=True, default=3)
    company_id = fields.Many2one('res.company', string='Company', default=lambda s: s.env.company)
    per_year = fields.Boolean(string='Yearly')

    @api.depends('number_current', 'number_next', 'number_increment')
    def _get_number_next(self):
        for seq in self:
            if seq.years_ids:
                target_year = seq.years_ids.search([('sequence_id', '=', seq.id), ('current', '=', True)], limit=1)
                seq.number_next = target_year.number_next
                seq.number_current = target_year.number_current
            else:
                seq.number_next = seq.number_current + seq.number_increment
                seq.number_current = seq.number_current

    number_next = fields.Integer(string='Next Number', required=True, readonly=True,store=True, compute=_get_number_next)
    number_current = fields.Integer(string='Current Number', readonly=True, store=True, compute=_get_number_next)

    years_ids = fields.One2many(comodel_name='one.sequence.years', string='Years', inverse_name='sequence_id', ondelete="cascade")
    state = fields.Selection(selection=[('draft', 'Draft'), ('running', 'Running')], default='draft')
    STOCK_PICK_CODE = 'SP'
    SALE_ORDER_CODE = 'SO'
    PURCHASE_ORDER_CODE = 'PO'
    INDUSTRY_CODE = '/I'
    CATEGORY_CODE = '/C'
    PARTNER_CODE = '/P'
    STOCK_INCOME_CODE = '/I'
    STOCK_OUTGOING_CODE = '/O'

    @api.depends('used_for', 'use_level', 'stock_picking_code', 'partner_id', 'industry_id', 'category_id',
                 'stock_picking_type_id')
    @api.onchange('used_for', 'use_level', 'stock_picking_code', 'partner_id', 'industry_id', 'category_id',
                  'stock_picking_type_id')
    def _get_sequence_prefix(self):
        for seq in self:
            seq.prefix = self._sequence_prefix()

    def _sequence_prefix(self):
        for seq in self:
            if seq.years_ids:
                new_year = seq.years_ids.search([('sequence_id', '=', seq.id), ('current', '=', True)], limit=1)
                now_current_year = new_year.year_to.year
            else:
                now_current_year = date.today().year

            seq.stock_picking_type_id = False
            for_prefix = self.STOCK_PICK_CODE if seq.used_for == 'stock_picking' else self.SALE_ORDER_CODE if seq.used_for == 'sale' else \
                self.PURCHASE_ORDER_CODE if seq.used_for == 'purchase' else ''
            level_prefix = self.INDUSTRY_CODE if seq.use_level == 'industry' else self.CATEGORY_CODE if seq.use_level == 'category' else \
                self.PARTNER_CODE if seq.use_level == 'partner' else ''
            stock_prefix = (self.STOCK_INCOME_CODE if seq.stock_picking_code == 'incoming' else self.STOCK_OUTGOING_CODE if seq.stock_picking_code \
                                                                                                                            == 'outgoing' else
            '') if seq.used_for == 'stock_picking' else ''

            industry_prefix = ('{}'.format(seq.industry_id.code) if seq.use_level == 'industry' and seq.industry_id.code else '')

            category_prefix = ('{}'.format(seq.category_id.code) if seq.use_level == 'category' and seq.category_id.code else '')

            partner_prefix = ('{}'.format(seq.partner_id.partner_code) if seq.use_level == 'partner' and seq.partner_id.partner_code else '')

            lst_prefix = industry_prefix if seq.use_level == 'industry' else category_prefix if seq.use_level == 'category' else partner_prefix if seq.use_level == 'partner' else ''

            stock_picking_type_prefix = '/{}'.format(
                seq.stock_picking_type_id.stcode) if seq.stock_picking_type_id and seq.stock_picking_type_id.stcode else ''

            return '{for_prefix}{stock_prefix}{lst_prefix}{stock_picking_type_prefix}/{year}'.format(
                for_prefix=for_prefix,
                # level_prefix=level_prefix,
                stock_prefix=stock_prefix,
                lst_prefix=lst_prefix,
                stock_picking_type_prefix=stock_picking_type_prefix,
                year=now_current_year)

    @api.model
    def next_one_sequence(self, used_for, partner_id, stock_picking_code=None):
        main_sequence = False
        new_sequence = None
        if not stock_picking_code:
            seq_per_partner_domain = [('state', '=', 'running'), ('used_for', '=', used_for),
                                      ('use_level', '=', 'partner'),
                                      ('partner_id', '=', partner_id.id), ('company_id', '=', self.env.company.id)]
            seq_per_category_domain = [('state', '=', 'running'), ('used_for', '=', used_for),
                                       ('use_level', '=', 'category'),
                                       ('category_id', '=', partner_id.categ_id.id),
                                       ('company_id', '=', self.env.company.id)]
            seq_per_industry_domain = [('state', '=', 'running'), ('used_for', '=', used_for),
                                       ('use_level', '=', 'industry'),
                                       ('industry_id', '=', partner_id.industry_id.id),
                                       ('company_id', '=', self.env.company.id)]
        else:
            seq_per_partner_domain = [('state', '=', 'running'), ('stock_picking_code', '=', stock_picking_code),
                                      ('used_for', '=', used_for),
                                      ('use_level', '=', 'partner'),
                                      ('partner_id', '=', partner_id.id), ('company_id', '=', self.env.company.id)]
            seq_per_category_domain = [('state', '=', 'running'), ('stock_picking_code', '=', stock_picking_code),
                                       ('used_for', '=', used_for),
                                       ('use_level', '=', 'category'),
                                       ('category_id', '=', partner_id.categ_id.id),
                                       ('company_id', '=', self.env.company.id)]
            seq_per_industry_domain = [('state', '=', 'running'), ('stock_picking_code', '=', stock_picking_code),
                                       ('used_for', '=', used_for),
                                       ('use_level', '=', 'industry'),
                                       ('industry_id', '=', partner_id.industry_id.id),
                                       ('company_id', '=', self.env.company.id)]

        seq_per_partner = self.env['one.sequence'].search(seq_per_partner_domain)
        seq_per_category = self.env['one.sequence'].search(seq_per_category_domain)
        seq_per_industry = self.env['one.sequence'].search(seq_per_industry_domain)
        if seq_per_partner:
            main_sequence = seq_per_partner
            new_sequence = seq_per_partner._sequence_prefix() + '/%%0%sd' % seq_per_partner.padding % seq_per_partner.years_ids.search(
                [('sequence_id', '=', seq_per_partner.id), ('current', '=', True)], limit=1).number_next
        elif seq_per_category and not seq_per_partner:
            main_sequence = seq_per_category
            new_sequence = seq_per_category._sequence_prefix() + '/%%0%sd' % seq_per_category.padding % seq_per_category.years_ids.search(
                [('sequence_id', '=', seq_per_category.id), ('current', '=', True)], limit=1).number_next

        elif seq_per_industry and not seq_per_category and not seq_per_partner:
            main_sequence = seq_per_industry
            new_sequence = seq_per_industry._sequence_prefix() + '/%%0%sd' % seq_per_industry.padding % seq_per_industry.years_ids.search(
                [('sequence_id', '=', seq_per_industry.id), ('current', '=', True)], limit=1).number_next
        if main_sequence:
            self.update_one_sequence_next(main_sequence)
        return new_sequence

    def run_one_sequence(self):
        for record in self:
            self.env['one.sequence.years'].create({
                'sequence_id': record.id,
                'year_from': date(date.today().year, 1, 1),
                'year_to': date(date.today().year, 12, 31),
                'current': True,
                'number_next': record.number_next,
                'number_current': record.number_current, })
            record.state = 'running'

    def update_one_sequence_next(self, sequence_id):
        year_id = False
        if sequence_id.years_ids:
            year_id = sequence_id.years_ids.search([('sequence_id', '=', sequence_id.id), ('current', '=', True)], limit=1)
            new_current = year_id.number_current + sequence_id.number_increment
            new_next = new_current + sequence_id.number_increment
            if sequence_id.per_year:
                if year_id.year_to.year == datetime.now().year:
                    year_id.write({'number_current': new_current, 'number_next': new_next})
                if not year_id.year_to.year == datetime.now().year:
                    year_id.current = False
                    year_id = self.env['one.sequence.years'].create({
                        'sequence_id': sequence_id.id,
                        'year_from': date(date.today().year, 1, 1),
                        'year_to': date(date.today().year, 12, 31),
                        'current': True,
                        'number_next': 0 + sequence_id.number_increment,
                        'number_current': 0,
                    })
            else:
                if year_id.year_to.year == datetime.now().year:
                    year_id.write({'number_current': new_current, 'number_next': new_next})
                else:
                    year_id.current = False
                    year_id = self.env['one.sequence.years'].create({
                        'sequence_id': sequence_id.id,
                        'year_from': date(date.today().year, 1, 1),
                        'year_to': date(date.today().year, 12, 31),
                        'current': True,
                        'number_next': new_next,
                        'number_current': new_current,
                    })
        else:
            new_current = sequence_id.number_current + sequence_id.number_increment
            new_next = new_current + sequence_id.number_increment
            sequence_id.write({'number_current': new_current, 'number_next': new_next})
        return year_id

    @api.model
    def create(self, vals_list):
        previous_seq = self.search(
            [('used_for', '=', vals_list['used_for']), ('use_level', '=', vals_list['use_level']), ('partner_id', '=', vals_list['partner_id']),
             ('industry_id', '=', vals_list['industry_id']), ('category_id', '=', vals_list['category_id']),
             ('company_id', '=', vals_list['company_id']), ('stock_picking_type_id', '=', vals_list['stock_picking_type_id']), ])
        if previous_seq:
            raise ValidationError('Sequence with selected criteria already exist')
        else:
            res = super(OneSequence, self).create(vals_list)
            return res

    def write(self, vals):
        previous_seq = self.search(
            [('used_for', '=', vals['used_for'] if 'used_for' in vals else False),
             ('use_level', '=', vals['use_level'] if 'use_level' in vals else False),
             ('partner_id', '=', vals['partner_id'] if 'partner_id' in vals else False),
             ('industry_id', '=', vals['industry_id'] if 'industry_id' in vals else False),
             ('category_id', '=', vals['category_id'] if 'category_id' in vals else False),
             ('company_id', '=', vals['company_id'] if 'company_id' in vals else False),
             ('stock_picking_type_id', '=', vals['stock_picking_type_id'] if 'stock_picking_type_id' in vals else False), ])
        if previous_seq:
            raise ValidationError('Sequence with selected criteria already exist')
        else:
            res = super(OneSequence, self).write(vals)
            return res


class OneSequenceYears(models.Model):
    _name = 'one.sequence.years'

    sequence_id = fields.Many2one(comodel_name='one.sequence', string='Sequence', ondelete="cascade")
    year_from = fields.Date(string='From')
    year_to = fields.Date(string='To')
    current = fields.Boolean(string='Current', default=False, store=True)
    number_next = fields.Integer(string='Next Number', required=True, readonly=True)
    number_current = fields.Integer(string='Current Number', readonly=True, store=True)
