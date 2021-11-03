# -*- coding: utf-8 -*-
# from odoo import http


# class OneSilverCustomerTarget(http.Controller):
#     @http.route('/one_silver_customer_target/one_silver_customer_target/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_customer_target/one_silver_customer_target/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_customer_target.listing', {
#             'root': '/one_silver_customer_target/one_silver_customer_target',
#             'objects': http.request.env['one_silver_customer_target.one_silver_customer_target'].search([]),
#         })

#     @http.route('/one_silver_customer_target/one_silver_customer_target/objects/<model("one_silver_customer_target.one_silver_customer_target"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_customer_target.object', {
#             'object': obj
#         })
