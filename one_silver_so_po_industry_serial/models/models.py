# -*- coding: utf-8 -*-

#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

#
#

# from odoo import models, fields, api


# class one_silver_so_po_industry_serial(models.Model):
#     _name = 'one_silver_so_po_industry_serial.one_silver_so_po_industry_serial'
#     _description = 'one_silver_so_po_industry_serial.one_silver_so_po_industry_serial'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
