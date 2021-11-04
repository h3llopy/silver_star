# -*- coding: utf-8 -*-
# from odoo import http


# class OneSilverSale(http.Controller):
#     @http.route('/one_silver_sale/one_silver_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_sale/one_silver_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_sale.listing', {
#             'root': '/one_silver_sale/one_silver_sale',
#             'objects': http.request.env['one_silver_sale.one_silver_sale'].search([]),
#         })

#     @http.route('/one_silver_sale/one_silver_sale/objects/<model("one_silver_sale.one_silver_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_sale.object', {
#             'object': obj
#         })
