# -*- coding: utf-8 -*-

#  /**
#   * @author :ibralsmn
#   * @mailto : ibralsmn@onesolutionc.com
#   * @company : onesolutionc.com
#   * @project : international_center
#   * @module:  addons
#   * @file : controllers.py
#   * @created : 9/30/21, 3:25 PM
#
#  **/

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


# class OneSilverSequenceLimit(http.Controller):
#     @http.route('/one_silver_sequence_limit/one_silver_sequence_limit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_silver_sequence_limit/one_silver_sequence_limit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_silver_sequence_limit.listing', {
#             'root': '/one_silver_sequence_limit/one_silver_sequence_limit',
#             'objects': http.request.env['one_silver_sequence_limit.one_silver_sequence_limit'].search([]),
#         })

#     @http.route('/one_silver_sequence_limit/one_silver_sequence_limit/objects/<model("one_silver_sequence_limit.one_silver_sequence_limit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_silver_sequence_limit.object', {
#             'object': obj
#         })
