# -*- coding: utf-8 -*-
# from odoo import http


# class OneSilverPurchaseReports(http.Controller):
#     @http.route('/one_silver_purchase_reports/one_silver_purchase_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_purchase_reports/one_silver_purchase_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_purchase_reports.listing', {
#             'root': '/one_silver_purchase_reports/one_silver_purchase_reports',
#             'objects': http.request.env['one_silver_purchase_reports.one_silver_purchase_reports'].search([]),
#         })

#     @http.route('/one_silver_purchase_reports/one_silver_purchase_reports/objects/<model("one_silver_purchase_reports.one_silver_purchase_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_purchase_reports.object', {
#             'object': obj
#         })
