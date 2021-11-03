# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverConfirmActions(http.Controller):
#     @http.route('/one_silver_confirm_actions/one_silver_confirm_actions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_confirm_actions/one_silver_confirm_actions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_confirm_actions.listing', {
#             'root': '/one_silver_confirm_actions/one_silver_confirm_actions',
#             'objects': http.request.env['one_silver_confirm_actions.one_silver_confirm_actions'].search([]),
#         })

#     @http.route('/one_silver_confirm_actions/one_silver_confirm_actions/objects/<model("one_silver_confirm_actions.one_silver_confirm_actions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_confirm_actions.object', {
#             'object': obj
#         })
