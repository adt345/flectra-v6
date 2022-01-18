from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError
from flectra.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = ['mrp.production']


    qty_kekurangan = fields.Float(string='Qty Kekurangan',compute='_get_jumlah_qty_kekurangan',store=True)

    @api.multi
    @api.depends('finished_move_line_ids')
    def _get_jumlah_qty_kekurangan(self):
        for production_id in self:
            production_id.qty_kekurangan = production_id.product_qty - production_id.total_qty_done