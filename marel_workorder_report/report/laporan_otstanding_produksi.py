from flectra import models, fields, api
from datetime import datetime, date
from flectra import http
from flectra.http import content_disposition, request
import io
import xlsxwriter
# from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT

class LaporanOtstandingProduksi(models.Model):
    _name = 'laporan.otstanding.produksi'
    _description = 'Laporan Otstanding Produksi'

    
    name = fields.Char(string='Report Otstanding', required=True, )
    date_start = fields.Datetime(string="Tanggal Awal", required=True, )
    date_end = fields.Datetime(string="Tanggal Akhir", required=True, )


    def generate_report(self):
        sql = """select
                    mp.id,
                    mp.name, 
                    pt.description, 
                    mp.product_qty, 
                    uu.name,
                    mw.jumlah_selesai_wo

                from mrp_production mp
                    Left join product_product pp on sq.product_id = pp.id
                    Left join product_template pt on pp.product_tmpl_id = pt.id
                    Left join uom_uom uu on pt.uom_id = uu.id
                    Left join mrp_workorder mw on mw.production_id = mp.id
                    left join stock_move_line sml on sml.production_id = mp.id
                where
                    and sq.in_date between %s and %s
                GROUP BY 
                sq.id,
                sl.id,
                pp.id,
                pt.id,
                pc.id
            """