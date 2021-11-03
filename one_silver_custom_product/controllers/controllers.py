# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverCustomProduct(http.Controller):
#     @http.route('/one_silver_custom_product/one_silver_custom_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_custom_product/one_silver_custom_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_custom_product.listing', {
#             'root': '/one_silver_custom_product/one_silver_custom_product',
#             'objects': http.request.env['one_silver_custom_product.one_silver_custom_product'].search([]),
#         })

#     @http.route('/one_silver_custom_product/one_silver_custom_product/objects/<model("one_silver_custom_product.one_silver_custom_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_custom_product.object', {
#             'object': obj
#         })
