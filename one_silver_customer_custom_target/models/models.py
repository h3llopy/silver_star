# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class one_silver_customer_custom_target(models.Model):
#     _name = 'one_silver_customer_custom_target.one_silver_customer_custom_target'
#     _description = 'one_silver_customer_custom_target.one_silver_customer_custom_target'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
