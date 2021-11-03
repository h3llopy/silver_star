# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverCollection(http.Controller):
#     @http.route('/one_silver_collection/one_silver_collection/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_collection/one_silver_collection/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_collection.listing', {
#             'root': '/one_silver_collection/one_silver_collection',
#             'objects': http.request.env['one_silver_collection.one_silver_collection'].search([]),
#         })

#     @http.route('/one_silver_collection/one_silver_collection/objects/<model("one_silver_collection.one_silver_collection"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_collection.object', {
#             'object': obj
#         })
