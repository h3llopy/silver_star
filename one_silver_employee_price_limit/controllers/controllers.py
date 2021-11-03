# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverEmployeePriceLimit(http.Controller):
#     @http.route('/one_silver_employee_price_limit/one_silver_employee_price_limit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_employee_price_limit/one_silver_employee_price_limit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_employee_price_limit.listing', {
#             'root': '/one_silver_employee_price_limit/one_silver_employee_price_limit',
#             'objects': http.request.env['one_silver_employee_price_limit.one_silver_employee_price_limit'].search([]),
#         })

#     @http.route('/one_silver_employee_price_limit/one_silver_employee_price_limit/objects/<model("one_silver_employee_price_limit.one_silver_employee_price_limit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_employee_price_limit.object', {
#             'object': obj
#         })
