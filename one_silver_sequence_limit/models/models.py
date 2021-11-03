# -*- coding: utf-8 -*-

#  /**
#   * @author :ibralsmn
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : international_center
#   * @module:  addons
#   * @file : models.py
#   * @created : 9/30/21, 3:25 PM
#
#  **/


# from odoo import models, fields, api


# class one_silver_sequence_limit(models.Model):
#     _name = 'one_silver_sequence_limit.one_silver_sequence_limit'
#     _description = 'one_silver_sequence_limit.one_silver_sequence_limit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
