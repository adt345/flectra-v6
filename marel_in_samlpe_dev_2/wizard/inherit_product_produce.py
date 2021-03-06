# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from collections import Counter
from datetime import datetime

from flectra import api, fields, models, _
from flectra.addons import decimal_precision as dp
from flectra.exceptions import UserError, ValidationError
from flectra.tools import float_compare, float_round

class MrpProductProduce(models.TransientModel):
    _name = "mrp.product.produce"
    _inherit = ["mrp.product.produce","mpc.abstract.produce"]


    @api.model
    def default_get(self, fields):
        res = super(MrpProductProduce, self).default_get(fields)
        if self._context and self._context.get('active_id'):
            production = self.env['mrp.production'].browse(self._context['active_id'])
            serial_finished = (production.product_id.tracking == 'serial')
            todo_uom = production.product_uom_id.id
            if serial_finished:
                todo_quantity = 1.0
                if production.product_uom_id.uom_type != 'reference':
                    todo_uom = self.env['product.uom'].search([('category_id', '=', production.product_uom_id.category_id.id), ('uom_type', '=', 'reference')]).id
            else:
                main_product_moves = production.move_finished_ids.filtered(lambda x: x.product_id.id == production.product_id.id)
                todo_quantity = production.product_qty - sum(main_product_moves.mapped('quantity_done'))
                todo_quantity = todo_quantity if (todo_quantity > 0) else 0
            if 'production_id' in fields:
                res['production_id'] = production.id
            if 'product_id' in fields:
                res['product_id'] = production.product_id.id
            if 'product_uom_id' in fields:
                res['product_uom_id'] = todo_uom
            if 'serial' in fields:
                res['serial'] = bool(serial_finished)
            if 'product_qty' in fields:
                res['product_qty'] = todo_quantity
        return res

    serial = fields.Boolean('Requires Serial')
    # stich = fields.Integer(related="nama_produk.stich",string='Stich',)
    time_bordir = fields.Integer(related="product_id.time_bordir", string='Time Bordir')
    karyawan = fields.Many2one('hr.employee', string="Operator", )
    time_real = fields.Integer(string ='Waktu Real/Menit', )
    shift = fields.Selection([
         ('A',_('A')),
         ('B',_('B')),
         ('C',_('C')),
    ], string= "Shif", )
    # production_id = fields.Many2one('mrp.production', 'Production')
    # product_id = fields.Many2one('product.product', 'Product')
    # product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True)
    # product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    # lot_id = fields.Many2one('stock.production.lot', domain="[('product_id', '=', product_id)]", string='Lot/Serial Number')
    produce_line_ids = fields.One2many('mrp.product.produce.line', 'product_produce_id', string='Product to Track')
    product_tracking = fields.Selection(related="product_id.tracking", readonly=True)
    stich = fields.Integer(related="product_id.stich", string="Stich", store=True, readonly=True)
    stich_jalan = fields.Integer(string='Stich Jalan', )

    
    # date_entry = fields.Datetime('Date', default=fields.Datetime.now)
    # net_weight = fields.Float(string='NW')
    # grade_id = fields.Char(string="Grade")
    # ket_grade = fields.Char(string='Keterangan Grade',)
    # justcut = fields.Char(string='Justcut',)
    # no_inspek = fields.Many2one ('mpc.inspek', string='No Inspek')
    
    # # total_point = fields.Float(string='Total Point')
    # shift_inspek = fields.Char(string='Shift Inspek', )
    # jumlah_inspek = fields.Integer(string='Jumlah Inspek', )
    # inspek = fields.Char(string='Inspektor',)
    # p1 = fields.Integer(string='Point 1', default=0)
    # p2 = fields.Integer(string='Point 2', default=0)
    # p3 = fields.Integer(string='Point 3', default=0)
    # p4 = fields.Integer(string='Point 4', default=0)
    # pd = fields.Integer(string='PD', default=0)
    # no_potong = fields.Many2one('mpc.weaving', string='Id Potong')
    # potongke = fields.Char(string='No Potong')
    # tgl_potong = fields.Date(string='Tgl Potong')
    # no_mesin = fields.Many2one('mesin.produksi', string='No Mesin')
    # shift = fields.Char(string='Shift Potong', )
    

    @api.multi
    def do_produce(self, context=None):
        # Nothing to do for lots since values are created using default data (stock.move.lots)
        quantity = self.product_qty
        if float_compare(quantity, 0, precision_rounding=self.product_uom_id.rounding) <= 0:
            raise UserError(_("The production order for '%s' has no quantity specified.") % self.product_id.display_name)
        for move in self.production_id.move_finished_ids:
            if move.product_id.tracking == 'none' and move.state not in ('done', 'cancel'):
                rounding = move.product_uom.rounding
                if move.product_id.id == self.production_id.product_id.id:
                    move.quantity_done += float_round(quantity, precision_rounding=rounding)
                elif move.unit_factor:
                    # byproducts handling
                    move.quantity_done += float_round(quantity * move.unit_factor, precision_rounding=rounding)
        self.check_finished_move_lots()

        if self.production_id.state == 'confirmed':
            self.production_id.write({
                'state': 'progress',
                'date_start': datetime.now(),
            })
        return {
            'type': 'ir.actions.act_window_close',
            # 'type':'ir.actions.report',
            # 'report_name':'in_report_mrp_mo.report_lot_stock_move_line',
            # 'model':'stock.production.lot',
            # 'report_type':"qweb-pdf",
            # 'ids': self.lot_id.id
            
        }

    @api.multi
    def check_finished_move_lots(self):
        produce_move = self.production_id.move_finished_ids.filtered(lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel'))
        if produce_move and produce_move.product_id.tracking != 'none':
            if not self.lot_id:
                raise UserError(_('You need to provide a lot for the finished product.'))
            existing_move_line = produce_move.move_line_ids.filtered(lambda x: x.lot_id == self.lot_id)
            if existing_move_line:
                if self.product_id.tracking == 'serial':
                    raise UserError(_('You cannot produce the same serial number twice.'))
                produced_qty = self.product_uom_id._compute_quantity(self.product_qty, existing_move_line.product_uom_id)
                existing_move_line.product_uom_qty += produced_qty
                existing_move_line.qty_done += produced_qty
            else:
                location_dest_id = produce_move.location_dest_id.get_putaway_strategy(self.product_id).id or produce_move.location_dest_id.id
                vals = {
                  'move_id': produce_move.id,
                  'product_id': produce_move.product_id.id,
                  'production_id': self.production_id.id,
                  'product_uom_qty': self.product_qty,
                  'product_uom_id': self.product_uom_id.id,
                  'qty_done': self.product_qty,
                  'lot_id': self.lot_id.id,
                  'location_id': produce_move.location_id.id,
                  'location_dest_id': location_dest_id,
                  'stich' : self.stich,
                  'time_real':self.time_real,
                  'shift':self.shift,
                #   'nw_done' : self.net_weight,
                #   'no_ins_done' : self.no_inspek.id,
                #   'no_beam_id' : self.no_beam_id.id,
                # #   'tot_po_done' : self.total_point,
                #   'grade_id_done' :  self.grade_id,
                #   'date' : self.date_entry,
                }
                self.env['stock.move.line'].create(vals)

            #tambahan move lot, inspek, weaving
            record_ids = self.env['stock.production.lot'].search([('id', '=', self.lot_id.id)])
            for record in record_ids:
                record.write({
                    'stich' : self.stich,
                    'time_real':self.time_real,
                    'shift':self.shift,
                    'karyawan':self.karyawan.id,
                    'no_mo': self.production_id.id,
                })

            # record_ids = self.env['mpc.inspek'].search([('id', '=', self.no_inspek.id)])
            # for record in record_ids:
            #     record.write({
            #         'kp_ins': self.production_id.id,
            #         'no_potong': self.no_potong.id,
            #         'shift_inspek': self.shift_inspek,
            #         'jumlah_inspek': self.jumlah_inspek,
            #         'inspek': self.inspek,
            #         'p1': self.p1,
            #         'p2': self.p2,
            #         'p3': self.p3,
            #         'p4': self.p4,
            #         'pd': self.pd,
            #         'ket_grade': self.ket_grade,
            #         'lbr_actual':self.lbr_actual,
            #     })

        for pl in self.produce_line_ids:
            if pl.qty_done:
                if pl.product_id.tracking != 'none' and not pl.lot_id:
                    raise UserError(_('Please enter a lot or serial number for %s !' % pl.product_id.display_name))
                if not pl.move_id:
                    # Find move_id that would match
                    move_id = self.production_id.move_raw_ids.filtered(lambda m: m.product_id == pl.product_id and m.state not in ('done', 'cancel'))
                    if move_id:
                        pl.move_id = move_id
                    else:
                        # create a move and put it in there
                        order = self.production_id
                        pl.move_id = self.env['stock.move'].create({
                                    'name': order.name,
                                    'product_id': pl.product_id.id,
                                    'product_uom': pl.product_uom_id.id,
                                    'location_id': order.location_src_id.id,
                                    'location_dest_id': self.product_id.property_stock_production.id,
                                    'raw_material_production_id': order.id,
                                    'group_id': order.procurement_group_id.id,
                                    'origin': order.name,
                                    'state': 'confirmed'})
                pl.move_id._generate_consumed_move_line(pl.qty_done, self.lot_id, lot=pl.lot_id)
        return True

    @api.onchange('product_qty')
    def _onchange_product_qty(self):
        lines = []
        qty_todo = self.product_uom_id._compute_quantity(self.product_qty, self.production_id.product_uom_id, round=False)
        for move in self.production_id.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.bom_line_id):
            qty_to_consume = float_round(qty_todo * move.unit_factor, precision_rounding=move.product_uom.rounding)
            for move_line in move.move_line_ids:
                if float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) <= 0:
                    break
                if move_line.lot_produced_id or float_compare(move_line.product_uom_qty, move_line.qty_done, precision_rounding=move.product_uom.rounding) <= 0:
                    continue
                to_consume_in_line = min(qty_to_consume, move_line.product_uom_qty)
                lines.append({
                    'move_id': move.id,
                    'qty_to_consume': to_consume_in_line,
                    'qty_done': to_consume_in_line,
                    'lot_id': move_line.lot_id.id,
                    'product_uom_id': move.product_uom.id,
                    'product_id': move.product_id.id,
                    'qty_reserved': min(to_consume_in_line, move_line.product_uom_qty),
                })
                qty_to_consume -= to_consume_in_line
            if float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) > 0:
                if move.product_id.tracking == 'serial':
                    while float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) > 0:
                        lines.append({
                            'move_id': move.id,
                            'qty_to_consume': 1,
                            'qty_done': 1,
                            'product_uom_id': move.product_uom.id,
                            'product_id': move.product_id.id,
                        })
                        qty_to_consume -= 1
                else:
                    lines.append({
                        'move_id': move.id,
                        'qty_to_consume': qty_to_consume,
                        'qty_done': qty_to_consume,
                        'product_uom_id': move.product_uom.id,
                        'product_id': move.product_id.id,
                    })

        self.produce_line_ids = [(5,)] + [(0, 0, x) for x in lines]


    def action_generate_serial(self):
        self.ensure_one()
        product_produce_wiz = self.env.ref('mrp.view_mrp_product_produce_wizard', False)
        self.lot_id = self.env['stock.production.lot'].create({
            'product_id': self.product_id.id,
        })
        return {
            'name': _('Produce'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.product.produce',
            'res_id': self.id,
            'view_id': product_produce_wiz.id,
            'target': 'new',
        }

    # def action_generate_inspek(self):
    #     self.ensure_one()
    #     product_produce_wiz = self.env.ref('mrp.view_mrp_product_produce_wizard', False)
    #     self.no_inspek = self.env['mpc.inspek'].create({
    #         'kp_ins': self.production_id.id,
    #     })
    #     return {
    #         'name': _('Produce'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'mrp.product.produce',
    #         'res_id': self.id,
    #         'view_id': product_produce_wiz.id,
    #         'target': 'new',
    #     }

    # @api.multi
    # def print_report(self, data):
    #     data = self.env.context.get('active_ids', [])
    #     return self.env.ref('mpc.action_report_produce_barcode').report_action(self, data=data)

    # @api.onchange('lot_id','no_inspek')
    # def _onchange_lotid(self):
    #     self.net_weight=self.lot_id.nw_done
    #     self.grade_id=self.lot_id.grade_id_done
    #     self.ket_grade=self.lot_id.ket_grade
    #     self.justcut=self.lot_id.justcut
    #     self.no_inspek=self.lot_id.no_ins_done.id

    #     self.shift_inspek=self.no_inspek.shift_inspek
    #     self.jumlah_inspek=self.no_inspek.jumlah_inspek 
    #     self.inspek=self.no_inspek.inspek
    #     self.p1=self.no_inspek.p1
    #     self.p2=self.no_inspek.p1
    #     self.p3=self.no_inspek.p1
    #     self.p4=self.no_inspek.p1
    #     self.pd=self.no_inspek.p1
    #     self.no_potong=self.no_inspek.no_potong.id

    #     self.potongke = self.no_potong.potongke
    #     self.tgl_potong = self.no_potong.tgl_potong
    #     self.no_mesin = self.no_potong.no_mesin.id
    #     self.shift = self.no_potong.shift

    # @api.onchange('no_potong')
    # def _onchange_nopot(self):
    #     self.potongke = self.no_potong.potongke
    #     self.tgl_potong = self.no_potong.tgl_potong
    #     self.no_mesin = self.no_potong.no_mesin.id
    #     self.shift = self.no_potong.shift


class MrpProductProduceLine(models.TransientModel):
    _name = "mrp.product.produce.line"
    _inherit = ["mrp.product.produce.line","mpc.abstract.produce.line"]

    product_produce_id = fields.Many2one('mrp.product.produce')
    # product_id = fields.Many2one('product.product', 'Product')
    # product_tracking = fields.Selection(related="product_id.tracking")
    # lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number')
    # qty_to_consume = fields.Float('To Consume', digits=dp.get_precision('Product Unit of Measure'))
    # product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    # qty_done = fields.Float('Consumed', digits=dp.get_precision('Product Unit of Measure'))
    # move_id = fields.Many2one('stock.move')
    # qty_reserved = fields.Float('Reserved', digits=dp.get_precision('Product Unit of Measure'))

    # @api.onchange('lot_id')
    # def _onchange_lot_id(self):
    #     """ When the user is encoding a produce line for a tracked product, we apply some logic to
    #     help him. This onchange will automatically switch `qty_done` to 1.0.
    #     """
    #     res = {}
    #     if self.product_id.tracking == 'serial':
    #         self.qty_done = 1
    #     return res

    # @api.onchange('qty_done')
    # def _onchange_qty_done(self):
    #     """ When the user is encoding a produce line for a tracked product, we apply some logic to
    #     help him. This onchange will warn him if he set `qty_done` to a non-supported value.
    #     """
    #     res = {}
    #     if self.product_id.tracking == 'serial' and self.qty_done:
    #         if float_compare(self.qty_done, 1.0, precision_rounding=self.move_id.product_id.uom_id.rounding) != 0:
    #             message = _('You can only process 1.0 %s of products with unique serial number.') % self.product_id.uom_id.name
    #             res['warning'] = {'title': _('Warning'), 'message': message}
    #     return res

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     self.product_uom_id = self.product_id.uom_id.id# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

# from collections import Counter
# from datetime import datetime

# from flectra import api, fields, models, _
# from flectra.addons import decimal_precision as dp
# from flectra.exceptions import UserError, ValidationError
# from flectra.tools import float_compare, float_round

# class InheritMrpProductProduce(models.TransientModel):
#     _name = "mrp.product.produce"
#     _inherit = ["mrp.product.produce",]
    

#     stich = fields.Integer(related="product_id.stich", string="Stich", store=True, readonly=True)
#     # sample_ ordir = fields.One2many("sample.bordir","product_id")
#     # stich = fields.Integer(related='product_id.stich',string='Stich')
#     def action_generate_serial(self):
#         self.ensure_one()
#         product_produce_wiz = self.env.ref('mrp.view_mrp_product_produce_wizard', False)
#         self.lot_id = self.env['stock.production.lot'].create({
#             'product_id': self.product_id.id,
#         })
#         return {
#             'name': _('Produce'),
#             'type': 'ir.actions.act_window',
#             'view_mode': 'form',
#             'res_model': 'mrp.product.produce',
#             'res_id': self.id,
#             'view_id': product_produce_wiz.id,
#             'target': 'new',
#         }