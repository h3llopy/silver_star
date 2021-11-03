# -*- coding: utf-8 -*-

#
#  @author : ibralsmn [bralsmn@gmail.com]
#  @filename : nagm-fady-new / controllers.py
#  @date : 9/23/21, 9:50 AM
#  Copyright (c) 2021. All rights reserved.
#

# from odoo import http


# class OneSilverDomainAddress(http.Controller):
#     @http.route('/one_silver_domain_address/one_silver_domain_address/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_domain_address/one_silver_domain_address/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_domain_address.listing', {
#             'root': '/one_silver_domain_address/one_silver_domain_address',
#             'objects': http.request.env['one_silver_domain_address.one_silver_domain_address'].search([]),
#         })

#     @http.route('/one_silver_domain_address/one_silver_domain_address/objects/<model("one_silver_domain_address.one_silver_domain_address"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_domain_address.object', {
#             'object': obj
#         })
