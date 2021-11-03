# -*- coding: utf-8 -*-

#  /**
#   * @author : ${USER}
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : ${PROJECT_NAME}
#   * @created : ${DATE}, ${DAY_NAME_FULL}
#   * @package : ${PACKAGE_NAME}
#  **/

#
#

# from odoo import http


# class OneSilverSoPoIndustrySerial(http.Controller):
#     @http.route('/one_silver_so_po_industry_serial/one_silver_so_po_industry_serial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_so_po_industry_serial/one_silver_so_po_industry_serial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_so_po_industry_serial.listing', {
#             'root': '/one_silver_so_po_industry_serial/one_silver_so_po_industry_serial',
#             'objects': http.request.env['one_silver_so_po_industry_serial.one_silver_so_po_industry_serial'].search([]),
#         })

#     @http.route('/one_silver_so_po_industry_serial/one_silver_so_po_industry_serial/objects/<model("one_silver_so_po_industry_serial.one_silver_so_po_industry_serial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_so_po_industry_serial.object', {
#             'object': obj
#         })
