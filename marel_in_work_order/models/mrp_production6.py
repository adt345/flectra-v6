from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError
from flectra.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = ['mrp.production']

    total_qty_done = fields.Integer(string='Total Done',compute='_get_jumlah_total_done',store=True)

    @api.multi
    @api.depends('finished_move_line_ids')
    def _get_jumlah_total_done(self):
        for production_id in self:
            production_id.total_qty_done = sum((line_id.qty_done) for line_id in production_id.finished_move_line_ids)