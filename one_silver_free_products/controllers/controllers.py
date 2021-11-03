# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverFreeProducts(http.Controller):
#     @http.route('/one_silver_free_products/one_silver_free_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_free_products/one_silver_free_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_free_products.listing', {
#             'root': '/one_silver_free_products/one_silver_free_products',
#             'objects': http.request.env['one_silver_free_products.one_silver_free_products'].search([]),
#         })

#     @http.route('/one_silver_free_products/one_silver_free_products/objects/<model("one_silver_free_products.one_silver_free_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_free_products.object', {
#             'object': obj
#         })
