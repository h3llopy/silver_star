# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverCustomerLimit(http.Controller):
#     @http.route('/one_silver_customer_limit/one_silver_customer_limit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_customer_limit/one_silver_customer_limit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_customer_limit.listing', {
#             'root': '/one_silver_customer_limit/one_silver_customer_limit',
#             'objects': http.request.env['one_silver_customer_limit.one_silver_customer_limit'].search([]),
#         })

#     @http.route('/one_silver_customer_limit/one_silver_customer_limit/objects/<model("one_silver_customer_limit.one_silver_customer_limit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_customer_limit.object', {
#             'object': obj
#         })
