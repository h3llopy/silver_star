from odoo import api, fields, models,_
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class expiry(models.Model):

    _inherit = 'stock.production.lot'
    expiry_check = fields.Selection(string="Lot Status", default='e' ,selection=[('e', 'Expired'), ('n', 'No'), ], required=False, )

    def expiry(self):
        
        today=fields.Datetime.today()
        search = self.env['stock.production.lot'].search([('removal_date', '<=', today)])
           
        print("search",search)
        print("today",today)
        for x in search:

            values={
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary':"expration",
                    'date_deadline': today,
                    'user_id':self.env.uid,
                    'note':"The lot is expiry",
                'res_model_id': self.env['ir.model'].search([('model', '=', 'stock.production.lot')]).id,
                'res_id': x.id,

                 }

            activity=self.env['mail.activity'].create(values)
            print(activity)
            search_scrap = self.env['stock.scrap'].search([('product_id','=',x.product_id.id),('lot_id','=',x.id)])
            if not search_scrap:
                
                search_quant=self.env['stock.quant'].search([('product_id','=',x.product_id.id),('lot_id','=',x.id),('location_id.usage','=','internal')])
                if search_quant:
                    search_location=self.env['stock.location'].search([('scrap_location', '=', True) ],limit=1)
                    scrap=self.env['stock.scrap'].create({
                        'product_id': x.product_id.id,
                        'scrap_qty':x.product_qty,
                        'lot_id': x.id,
                        'location_id': search_quant.location_id.id,
                        'scrap_location_id':search_location.id,
                        'product_uom_id': x.product_id.uom_id.id,

                    })
            
                #vals = {
                #'product_id': x.product_id.id,
                #'scrap_qty':x.product_qty,
                #'lot_id': x.id,
                #'location_id': 8,
                #'scrap_location_id': 16,

            #}
            #scrap=self.env['stock.scrap'].create(vals)
            #scrap.do_scrap()
            #print(scrap)


class ExpiryDateWarning(models.Model):
    _inherit = 'sale.order.line'
    @api.onchange('product_id', 'product_uom_qty')
    def product_uom_change(self):

        if self.product_id:
            total_quantity = 0.0
            product_sale = self.product_id
            quantity_in_lot = self.env['stock.quant'].search([])
            lot_search = self.env['stock.production.lot']
            lot_number_obj = lot_search.search([])
            for x in lot_number_obj:
                # date = date.today()

                if x.expiration_date:
                    dates = datetime.strptime(str(x.expiration_date), '%Y-%m-%d %H:%M:%S')

                if x.product_id.id == product_sale.id:
                    if x.expiration_date and x.expiration_date.date() < date.today():
                        for values in quantity_in_lot:
                            if values.lot_id.id == x.id and values.product_id.id == product_sale.id:
                                if values.quantity >= 0:
                                    total_quantity = total_quantity + values.quantity
                    # elif x.product_id.id == product_sale.id and dates.date() is False:
                #     raise ValidationError(_("Set lot number and expiration date."))
            good_products = self.product_id.qty_available - total_quantity


            search = self.env['stock.production.lot'].search(
                [('product_id', '=', self.product_id.id), ('alert_date', '<=', date.today())])
            for x in search:
                if x.product_expiry_alert == True:
                    if good_products < self.product_uom_qty:
                        if self.product_id.type == 'product':

                            name = x.name
                            name_of_lots = ''
                            for x in search:
                                if name_of_lots == '':
                                    name_of_lots = x.name
                                else:
                                    name_of_lots = name_of_lots + "," + x.name
                                print(x)

                            raise UserError(_('some lots are expired! : %s' % name_of_lots))

            if good_products < self.product_uom_qty:
                if self.product_id.type == 'product':
                    warning = {
                        'title': _('not enough quantity in stock'),
                        'message': _(
                            'The demand quantity is over on hand quantity in this warehouse')
                    }
                    return {'warning': warning}

    @api.onchange('price_unit')
    def sale_cost(self):


        if self.price_unit < self.product_id.standard_price:
            if self.env.user.has_group('product_expired_v14.group_expiry_validation'):
                raise ValidationError('Cost cant be bigger than the Unit Price',)


            if self.env.user.has_group('product_expired_v14.group_expiry_warning') :
                return {'warning': {'title': _("Warning"), 'message': "the Cost cant be bigger than the Unit Price"}}
