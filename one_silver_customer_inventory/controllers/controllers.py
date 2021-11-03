# -*- coding: utf-8 -*-
# from odoo import http


# class OneSilverCustomerInventory(http.Controller):
#     @http.route('/one_silver_customer_inventory/one_silver_customer_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_customer_inventory/one_silver_customer_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_customer_inventory.listing', {
#             'root': '/one_silver_customer_inventory/one_silver_customer_inventory',
#             'objects': http.request.env['one_silver_customer_inventory.one_silver_customer_inventory'].search([]),
#         })

#     @http.route('/one_silver_customer_inventory/one_silver_customer_inventory/objects/<model("one_silver_customer_inventory.one_silver_customer_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_customer_inventory.object', {
#             'object': obj
#         })
