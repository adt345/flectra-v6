from flectra.addons import decimal_precision as dp
from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError
from datetime import date, datetime
from flectra.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from flectra.tools import float_round

class MarelInSamlpeDev2List(models.Model):
    _name = 'marelin.samlpe.dev2.list'

    marel_in_samlpe_dev_id = fields.Many2one('marelin.samlpe.dev2',string=u'marel in samlpe_dev id', store=True)
    #------------
    product_id = fields.Many2one('product.product',string=u'Nama Benang', store=True)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil (C)', store=True)
    qty_benang_kg = fields.Float(string=u'Qty Benang Per Pasang (kg)',digits=dp.get_precision('Custom 2'), store=True)
    qty_benang_gr = fields.Float(string=u'Qty Benang Per Pasang (gr)',digits=dp.get_precision('Custom 2'), store=True)
    qty_bom_reguler = fields.Float(string=u'Qty Bom (R)',digits=dp.get_precision('Custom 2'), store=True)
    qty_bom_soccer = fields.Float(string=u'Qty Bom (S)',digits=dp.get_precision('Custom 2'), store=True)
    partner_id = fields.Many2one('res.partner', string='Customer', )
    awal = fields.Float(string=u'Awal',digits=dp.get_precision('Custom 2'), store=True)
    akhir = fields.Float(string=u'Akhir',digits=dp.get_precision('Custom 2'), store=True)
    terpakai = fields.Float(string=u'Terpakai',digits=dp.get_precision('Custom 2'), store=True)

    @api.multi
    def get_hitung_qty_bom_line(self):
        self.qty_bom_reguler = 0.0
        self.qty_bom_soccer = 0.0
        #mengconvert dari gr ke kg
        self.qty_benang_kg = (self.qty_benang_gr/1000)
        #perhitungan toleransi
        toleransi_qty_bom_r = (self.qty_benang_kg*0.07)
        toleransi_qty_bom_s = (self.qty_benang_kg*0.15)
        #qty bom kaos kaki
        self.qty_bom_reguler = (self.qty_benang_kg + toleransi_qty_bom_r)
        self.qty_bom_soccer = (self.qty_benang_kg + toleransi_qty_bom_s)
        return

class MarelInAksesorisSamlpeDev2List(models.Model):
    _name = 'marelin.aksesotis.samlpedev2.list'

    marel_in_samlpe_dev_id = fields.Many2one('marelin.samlpe.dev2',string=u'marel_in_samlpe_dev_id', store=True)
    #------------
    product_id = fields.Many2one('product.product',string=u'Nama Aksesoris', store=True)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil', store=True)


class OperatorMarelInSamlpeDev2List(models.Model):
    _name = 'operator.marelinsamlpe.dev2.list'

    marel_in_samlpe_dev_id = fields.Many2one('marelin.samlpe.dev2',string=u'marel_in_samlpe_dev_id', store=True)

    
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    nama_desain = fields.Char(string='Nama Desain', store=True)
    berat = fields.Char(string='Berat', store=True)
    waktu_produksi = fields.Char(string='Waktu Produksi', store=True)
    tgl_buat = fields.Date(string='Tgl Buat',default=fields.Date.context_today, store=True)
    nama_operator_id = fields.Many2one('marel.nama.operator',string=u'Nama Operator', store=True)


    gum_stretch_x= fields.Char(string='Gum Stretch x ', store=True)
    gum_stretch_y= fields.Char(string='Gum Stretch y ', store=True)
    leg_gum_stretch_x= fields.Char(string='Leg Gum Stretch x ', store=True)
    leg_gum_stretch_y= fields.Char(string='Leg Gum Stretch y ', store=True)
    leg_gum_atas_stretch_x= fields.Char(string='Leg Gum Atas Stretch x ', store=True)
    leg_gum_atas_stretch_y= fields.Char(string='Leg Gum Atas Stretch y ', store=True)
    leg_gum_bawah_stretch_x= fields.Char(string='Leg Gum Bawah Stretch x ', store=True)
    leg_gum_bawah_stretch_y= fields.Char(string='Leg Gum Bawah Stretch y ', store=True)
    leg_stretch_x= fields.Char(string=' Leg Stretch x', store=True)
    leg_stretch_y= fields.Char(string='Leg Stretch y ', store=True)
    foot_stretch_x= fields.Char(string=' Foot Stretch x', store=True)
    foot_stretch_y= fields.Char(string=' Foot Stretch y', store=True)
    foot_gum_stretch_x= fields.Char(string='Foot Gum Stretch x ', store=True)
    foot_gum_stretch_y= fields.Char(string='Foot Gum Stretch y ', store=True)
    hell_stretch_x= fields.Char(string='Heel Stretch x ', store=True)
    hell_stretch_y= fields.Char(string='Heel Stretch y ', store=True)

    #tambhan 190820------------------------
    gum_atas_stretch_x = fields.Char(string='Gum Atas Stretch X', store=True)
    gum_atas_stretch_y = fields.Char(string='Gum Atas Stretch Y', store=True)

    gum_bawah_stretch_x = fields.Char(string='Gum Bawah Stretch X', store=True)
    gum_bawah_stretch_y = fields.Char(string='Gum Bawah Stretch Y' , store=True)


    leg_gum_atas_stretch_x = fields.Char(string='Leg Gum Atas Stretch X', store=True)
    leg_gum_atas_stretch_y = fields.Char(string='Leg Gum Atas Stretch Y', store=True)
    
    leg_gum_bawah_stretch_x = fields.Char(string='Leg Gum Bawah Stretch X', store=True)
    leg_gum_bawah_stretch_y= fields.Char(string='Leg Gum Bawah Stretch Y', store=True)
    
    leg_gum_tengah_stretch_x = fields.Char(string='Leg Gum Tengah Stretch X', store=True)
    leg_gum_tengah_stretch_y = fields.Char(string='Leg Gum Tengah Stretch Y', store=True)

    # tutup tambhan 190820---------------------------------

    
    welt_inside_crc = fields.Char(string='Welt Inside CRC', store=True)
    welt_inside_s = fields.Char(string='Welt Inside S', store=True)
    welt_inside_e = fields.Char(string='Welt Inside E', store=True)

    welt_outside_crc = fields.Char(string='Welt Outside CRC', store=True)
    welt_outside_s = fields.Char(string='Welt Outside S', store=True)
    welt_outside_e = fields.Char(string='Welt Outside E', store=True)
    
    transfer_crc = fields.Char(string='Transfer CRC', store=True)
    transfer_s = fields.Char(string='Transfer S', store=True)
    transfer_e = fields.Char(string='Transfer E', store=True)

    leg_gum_crc = fields.Char(string='Leg Gum CRC', store=True)
    leg_gum_s = fields.Char(string='Leg Gum S', store=True)
    leg_gum_e = fields.Char(string='Leg Gum E', store=True)

    leg_crc = fields.Char(string='Leg CRC', store=True)
    leg_s = fields.Char(string='Leg S', store=True)
    leg_e = fields.Char(string='Leg E', store=True)

    leg_band_elast_crc = fields.Char(string='Leg band Elast CRC', store=True)
    leg_band_elast_s = fields.Char(string='Leg band Elast S', store=True)
    leg_band_elast_e = fields.Char(string='Leg band Elast E', store=True)

    ankle_crc = fields.Char(string='Ankle CRC', store=True)
    ankle_s = fields.Char(string='Ankle S', store=True)
    ankle_e = fields.Char(string='Ankle E', store=True)

    heel_crc = fields.Char(string='Heel CRC', store=True)
    heel_s = fields.Char(string='Heel S', store=True)
    heel_e = fields.Char(string='Heel E', store=True)

    foot_gum_crc = fields.Char(string='Foot Gum CRC', store=True)
    foot_gum_s = fields.Char(string='Foot Gum S', store=True)
    foot_gum_e = fields.Char(string='Foot Gum E', store=True)

    foot_crc = fields.Char(string='Foot CRC', store=True)
    foot_s = fields.Char(string='Foot S', store=True)
    foot_e = fields.Char(string='Foot E', store=True)

    begin_toe_crc = fields.Char(string='Begin Toe CRC', store=True)
    begin_toe_s = fields.Char(string='Begin Toe S', store=True)
    begin_toe_e = fields.Char(string='Begin Toe E', store=True)

    toe_crc = fields.Char(string='Toe CRC', store=True)
    toe_s = fields.Char(string='Toe S', store=True)
    toe_e = fields.Char(string='Toe E', store=True)

    rosso_crc = fields.Char(string='Rosso CRC', store=True)
    rosso_s = fields.Char(string='Rosso S', store=True)
    rosso_e = fields.Char(string='Rosso E', store=True)

    lose_crc = fields.Char(string='Lose CRC', store=True)
    lose_s = fields.Char(string='Lose S', store=True)
    lose_e = fields.Char(string='Lose E', store=True)

    lingking_crc = fields.Char(string='Lingking CRC', store=True)
    lingking_s = fields.Char(string='Lingking S', store=True)
    lingking_e = fields.Char(string='Lingking E', store=True)

    
    feed_1 = fields.Char(string='Feed 1', store=True)
    feed_1a = fields.Char(string='Feed 1A', store=True)
    feed_1b = fields.Char(string='Feed 1B', store=True)
    feed_1c = fields.Char(string='Feed 1C', store=True)

    feed_2 = fields.Char(string='Feed 2', store=True)
    feed_2a = fields.Char(string='Feed 2A', store=True)
    feed_2b = fields.Char(string='Feed 2B', store=True)
    feed_2c = fields.Char(string='Feed 2C', store=True)

    feed_3_a = fields.Char(string='Feed 3.A', store=True)
    feed_3a = fields.Char(string='Feed 3A', store=True)
    feed_3_b = fields.Char(string='Feed 3.B', store=True)
    feed_3b = fields.Char(string='Feed 3B', store=True)
    feed_3c = fields.Char(string='Feed 3C', store=True)

    feed_4_a = fields.Char(string='Feed 4.A', store=True)
    feed_4a = fields.Char(string='Feed 4A', store=True)
    feed_4_b = fields.Char(string='Feed 1', store=True)
    feed_4b = fields.Char(string='Feed 4B', store=True)

    feed_5 = fields.Char(string='Feed 5', store=True)
    feed_5a = fields.Char(string='Feed 5A', store=True)
    feed_5b = fields.Char(string='Feed 5B', store=True)
    feed_5c = fields.Char(string='Feed 5C', store=True)
    
    feed_6 = fields.Char(string='Feed 6', store=True)
    feed_7 = fields.Char(string='Feed 7', store=True)
    feed_8 = fields.Char(string='Feed 8', store=True)
    #tambhan yang dev 3
    tgl_buat_operator = fields.Date(string='Tgl Buat Operator', store=True)
    feed_4c = fields.Char(string='Feed 4C', store=True)

# --------------------------JENIS KAOS KAKI ---------------------------------------
class MarelInSamlpeJenisKk(models.Model):
    _name = 'marel.sample.jenis.kk'
    
    name = fields.Char(string='Name', store=True)
    

class MarelInSamlpeBom(models.Model):
    _inherit = ['mrp.bom']

    janis_kk_id = fields.Many2one('marel.sample.jenis.kk',string='Janis Kk',store=True,)
    
class MarelInSamlpeBomLine(models.Model):
    _inherit = ['mrp.bom.line']

    marel_in_samlpe_dev_id = fields.Many2one('marelin.samlpe.dev2',string=u'marel in samlpe_dev id', store=True)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil (C)', store=True)
    qty_benang_kg = fields.Float(string=u'Qty Benang Per Pasang (kg)',digits=dp.get_precision('Custom 2'), store=True)
    qty_benang_gr = fields.Float(string=u'Qty Benang Per Pasang (gr)',digits=dp.get_precision('Custom 2'), store=True)
    qty_bom_reguler = fields.Float(string=u'Qty Bom (R)',digits=dp.get_precision('Custom 2'), store=True)
    qty_bom_soccer = fields.Float(string=u'Qty Bom (S)',digits=dp.get_precision('Custom 2'), store=True)
    awal = fields.Float(string=u'Awal',digits=dp.get_precision('Custom 2'), store=True)
    akhir = fields.Float(string=u'Akhir',digits=dp.get_precision('Custom 2'), store=True)
    terpakai = fields.Float(string=u'Terpakai',digits=dp.get_precision('Custom 2'), store=True)


    @api.multi
    def get_hitung_qty_mrp_bom_line(self):
        self.qty_bom_reguler = 0.0
        self.qty_bom_soccer = 0.0
        #mengconvert dari gr ke kg
        self.qty_benang_kg = (self.qty_benang_gr/1000)
        #perhitungan toleransi
        toleransi_qty_bom_r = (self.qty_benang_kg*0.07)
        toleransi_qty_bom_s = (self.qty_benang_kg*0.15)
        #qty bom kaos kaki
        self.qty_bom_reguler = (self.qty_benang_kg + toleransi_qty_bom_r)
        self.qty_bom_soccer = (self.qty_benang_kg + toleransi_qty_bom_s)

        if (self.bom_id.janis_kk_id.id == 1):
            self.product_qty = self.qty_bom_reguler
        else :
            self.product_qty = self.qty_bom_soccer
        # else :
        #     self.product_qty = self.product_qty
        return


class MarelInSamlpeDev2(models.Model):

    _name = 'marelin.samlpe.dev2'
    _rec_name = 'product_id'

    marel_in_samlpe_dev_list_line = fields.One2many('marelin.samlpe.dev2.list','marel_in_samlpe_dev_id',string=u'Samlpe Dev Line', store=True)
    operator_marelinsamlpedev2_list = fields.One2many('operator.marelinsamlpe.dev2.list','marel_in_samlpe_dev_id',string=u'Oeprator Mengisi Sample', store=True)
    marelin_aksesotis_samlpedev2_list = fields.One2many('marelin.aksesotis.samlpedev2.list','marel_in_samlpe_dev_id',string=u'Aksesoris Samlpe Dev Line', store=True)
    # mrp bom
    bom_line_list = fields.One2many('mrp.bom.line','marel_in_samlpe_dev_id',string=u'BOM Line',related='product_id.bom_ids.bom_line_ids', store=True)


    def get_marelin_samlpe_dev2_no(self):
        nama_baru = self.env['ir.sequence'].next_by_code('marelin.samlpe.dev2.no')
        return nama_baru
      
    name = fields.Char(string='Id Sample',required=True,copy=False, default=get_marelin_samlpe_dev2_no,readonly=True )
    #-------------------------------------
    tgl_masuk = fields.Date(string=u'Tgl Masuk',default=fields.Date.context_today, store=True)
    tgl_selesai = fields.Datetime(string=u'Tgl Selesai',readonly=True)
    product_id = fields.Many2one('product.product',string=u'Nama Prodak', store=True)
    kode_dokumen = fields.Char(string=u'Kode Doc', store=True)
    gambar_sample = fields.Binary(string='Gambar Sample', store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    penjerat_2 = fields.Many2one('product.product',string=u'Penjerat 2', store=True)

    # steam
    size = fields.Float(string='Size', store=True)
    waktu = fields.Float(string='Waktu Steam', store=True)
    waktu_anti_slip = fields.Float(string='Waktu Anti Slip', store=True)
    keterangan_anti_slip = fields.Text(string='keterangan AS', store=True)


    no_mesin = fields.Float(string=u'No Mesin/Jarum', store=True)
    warna = fields.Char(string=u'Warna', store=True)
    keterangan = fields.Text(string='keterangan', store=True)
    
    brand = fields.Char(string=u'Brand', store=True)
    model_sample = fields.Char(string=u'Model', store=True)
    tipe = fields.Char(string=u'Type', store=True)
    delivery = fields.Datetime(string=u'Delivery', store=True)

    gum_relaxed_x= fields.Float(string='Gum Relaxed x ', store=True)
    gum_relaxed_y= fields.Float(string='Gum Relaxed y ', store=True)

    leg_gum_relaxed_x= fields.Float(string='Leg Gum Relaxed x ', store=True)
    leg_gum_relaxed_y= fields.Float(string='Leg Gum Relaxed y ', store=True)

    leg_gum_atas_relaxed_x= fields.Float(string='Leg Gum Atas Relaxed x ', store=True)
    leg_gum_atas_relaxed_y= fields.Float(string='Leg Gum Atas Relaxed y ', store=True)

    leg_gum_bawah_relaxed_x= fields.Float(string='Leg Gum Bawah Relaxed x ', store=True)
    leg_gum_bawah_relaxed_y= fields.Float(string='Leg Gum Bawah Relaxed y ', store=True)

    leg_relaxed_x= fields.Float(string=' Leg Relaxed x', store=True)
    leg_relaxed_y= fields.Float(string='Leg Relaxed y ', store=True)

    foot_relaxed_x= fields.Float(string=' Foot Relaxed x', store=True)
    foot_relaxed_y= fields.Float(string=' Foot Relaxed y', store=True)

    foot_gum_relaxed_x= fields.Float(string='Foot Gum Relaxed x ', store=True)
    foot_gum_relaxed_y= fields.Float(string='Foot Gum Relaxed y ', store=True)

    hell_relaxed_x= fields.Float(string='Heel Relaxed x ', store=True)
    hell_relaxed_y= fields.Float(string='Heel Relaxed y ', store=True)

    #tambhan 190820---------------------------------
    gum_atas_relaxed_x = fields.Float(string='Gum Atas Relaxed X', store=True)
    gum_atas_relaxed_y = fields.Float(string='Gum Atas Relaxed Y', store=True)

    gum_bawah_relaxed_x = fields.Float(string='Gum Bawah relaxed X', store=True)
    gum_bawah_relaxed_y = fields.Float(string='Gum Bawah Relaxed Y' , store=True)

    
    leg_gum_tengah_relaxed_x = fields.Float(string='Leg Gum Tengah Relaxed X', store=True)
    leg_gum_tengah_relaxed_y = fields.Float(string='Leg Gum Tengah Relaxed Y', store=True)
    

    style = fields.Char(string=u'Style', store=True)
    artikel = fields.Char(string=u'Artikel', store=True)
    body = fields.Many2one('product.product',string=u'Body', store=True)
    wording_munich = fields.Many2one('product.product',string=u'Wording', store=True)
    logo = fields.Many2one('product.product',string=u'Logo', store=True)
    hell = fields.Many2one('product.product',string=u'Heel', store=True)
    toe = fields.Many2one('product.product',string=u'Toe', store=True)
    transfer = fields.Many2one('product.product',string=u'Transfer', store=True)
    lintoe = fields.Many2one('product.product',string=u'Lintoe', store=True)
    penjerat = fields.Many2one('product.product',string=u'Penjerat', store=True)
    karet = fields.Many2one('product.product',string=u'Karet', store=True)
    patter_1 = fields.Many2one('product.product',string=u'Pattern 1', store=True)
    patter_2 = fields.Many2one('product.product',string=u'Pattern 2', store=True)
    patter_3 = fields.Many2one('product.product',string=u'Pattern 3', store=True)
    patter_4 = fields.Many2one('product.product',string=u'Pattern 4', store=True)
    patter_5 = fields.Many2one('product.product',string=u'Pattern 5', store=True)
    patter_6 = fields.Many2one('product.product',string=u'Pattern 6', store=True)
    patter_7 = fields.Many2one('product.product',string=u'Pattern 7', store=True)
    patter_8 = fields.Many2one('product.product',string=u'Pattern 8', store=True)
    patter_9 = fields.Many2one('product.product',string=u'Pattern 9', store=True)
    patter_10 = fields.Many2one('product.product',string=u'Pattern 10', store=True)
    jumlah_pasang = fields.Integer(string='Jumlah Pasang', store=True)

    #untuk BOM Benang
    needle = fields.Char(string=u'Needle', store=True)
    nama_sample = fields.Char(string=u'Nama Sample', store=True)
    tgl_bon = fields.Date(string=u'Tgl Permintaan BON',default=fields.Date.context_today, store=True)

    partner_id = fields.Many2one('res.partner', string='Customer', store=True)
    state = fields.Selection([
        ('draft', 'Open'),
        ('done','Done'),
        ('cancel','Canceled')
        ],string="Status", readonly=True, copy=False, default='draft')
                            
    @api.multi
    def action_close(self):
        tgl_selesai = fields.Datetime.now()
        self.write({'state': 'done','tgl_selesai':tgl_selesai})
        self._get_copy_data_sample()
        # return True

    @api.multi
    def action_set_draft(self):
        self.write({'state': 'draft'})
        self._get_copy_data_sample()
        # return True

    # TOTAL BRUTO
    total_bruto = fields.Float(string='Total Bruto',compute='_get_jumlah_total_bruto',store=True)

    @api.multi
    def _get_copy_data_sample(self):
        if self.product_id :
            self.product_id.product_tmpl_id.kode_dokumen = self.kode_dokumen
            self.product_id.product_tmpl_id.gambar_sample = self.gambar_sample
            self.product_id.product_tmpl_id.penjerat_2 = self.penjerat_2
            self.product_id.product_tmpl_id.size = self.size
            self.product_id.product_tmpl_id.waktu = self.waktu
            self.product_id.product_tmpl_id.waktu_anti_slip = self.waktu_anti_slip
            self.product_id.product_tmpl_id.keterangan_anti_slip = self.keterangan_anti_slip
            self.product_id.product_tmpl_id.warna = self.warna
            self.product_id.product_tmpl_id.keterangan = self.keterangan
            self.product_id.product_tmpl_id.brand = self.brand
            self.product_id.product_tmpl_id.model_sample = self.model_sample
            self.product_id.product_tmpl_id.tipe = self.tipe
            self.product_id.product_tmpl_id.gum_relaxed_x = self.gum_relaxed_x
            self.product_id.product_tmpl_id.gum_relaxed_y = self.gum_relaxed_y
            self.product_id.product_tmpl_id.leg_gum_relaxed_x = self.leg_gum_relaxed_x
            self.product_id.product_tmpl_id.leg_gum_relaxed_y = self.leg_gum_relaxed_y
            self.product_id.product_tmpl_id.leg_gum_atas_relaxed_x = self.leg_gum_atas_relaxed_x
            self.product_id.product_tmpl_id.leg_gum_atas_relaxed_y = self.leg_gum_atas_relaxed_y
            self.product_id.product_tmpl_id.leg_gum_bawah_relaxed_x = self.leg_gum_bawah_relaxed_x
            self.product_id.product_tmpl_id.leg_gum_bawah_relaxed_y = self.leg_gum_bawah_relaxed_y
            self.product_id.product_tmpl_id.leg_relaxed_x = self.leg_relaxed_x
            self.product_id.product_tmpl_id.leg_relaxed_y = self.leg_relaxed_y
            self.product_id.product_tmpl_id.foot_relaxed_x = self.foot_relaxed_x
            self.product_id.product_tmpl_id.foot_relaxed_y = self.foot_relaxed_y
            self.product_id.product_tmpl_id.foot_gum_relaxed_x = self.foot_gum_relaxed_x
            self.product_id.product_tmpl_id.foot_gum_relaxed_y = self.foot_gum_relaxed_y
            self.product_id.product_tmpl_id.hell_relaxed_x = self.hell_relaxed_x
            self.product_id.product_tmpl_id.hell_relaxed_y = self.hell_relaxed_y
            self.product_id.product_tmpl_id.gum_atas_relaxed_x = self.gum_atas_relaxed_x
            self.product_id.product_tmpl_id.gum_atas_relaxed_y = self.gum_atas_relaxed_y
            self.product_id.product_tmpl_id.gum_bawah_relaxed_x = self.gum_bawah_relaxed_x
            self.product_id.product_tmpl_id.gum_bawah_relaxed_y = self.gum_bawah_relaxed_y
            self.product_id.product_tmpl_id.leg_gum_tengah_relaxed_x = self.leg_gum_tengah_relaxed_x
            self.product_id.product_tmpl_id.leg_gum_tengah_relaxed_y = self.leg_gum_tengah_relaxed_y
            self.product_id.product_tmpl_id.style = self.style
            self.product_id.product_tmpl_id.artikel = self.artikel
            self.product_id.product_tmpl_id.body = self.body
            self.product_id.product_tmpl_id.wording_munich = self.wording_munich
            self.product_id.product_tmpl_id.logo = self.logo
            self.product_id.product_tmpl_id.hell = self.hell
            self.product_id.product_tmpl_id.toe = self.toe
            self.product_id.product_tmpl_id.transfer = self.transfer
            self.product_id.product_tmpl_id.lintoe = self.lintoe
            self.product_id.product_tmpl_id.penjerat = self.penjerat
            self.product_id.product_tmpl_id.karet = self.karet
            self.product_id.product_tmpl_id.patter_1 = self.patter_1
            self.product_id.product_tmpl_id.patter_2 = self.patter_2
            self.product_id.product_tmpl_id.patter_3 = self.patter_3
            self.product_id.product_tmpl_id.patter_4 = self.patter_4
            self.product_id.product_tmpl_id.patter_5 = self.patter_5
            self.product_id.product_tmpl_id.patter_6 = self.patter_6
            self.product_id.product_tmpl_id.patter_7 = self.patter_7
            self.product_id.product_tmpl_id.patter_8 = self.patter_8
            self.product_id.product_tmpl_id.patter_9 = self.patter_9
            self.product_id.product_tmpl_id.patter_10 = self.patter_10
            self.product_id.product_tmpl_id.needle = self.needle
            self.product_id.product_tmpl_id.nama_sample = self.nama_sample


    @api.multi
    @api.depends('bom_line_list')
    def _get_jumlah_total_bruto(self):
        for marel_in_samlpe_dev_id in self:
            marel_in_samlpe_dev_id.total_bruto = sum((line_id.terpakai) for line_id in marel_in_samlpe_dev_id.bom_line_list)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    kode_dokumen = fields.Char(string=u'Kode Doc', store=True)
    gambar_sample = fields.Binary(string='Gambar Sample', store=True)

    penjerat_2 = fields.Many2one('product.product',string=u'Penjerat 2', store=True)

    size = fields.Float(string='Size', store=True)
    waktu = fields.Float(string='Waktu Steam', store=True)
    waktu_anti_slip = fields.Float(string='Waktu Anti Slip', store=True)
    keterangan_anti_slip = fields.Text(string='keterangan AS', store=True)

    warna = fields.Char(string=u'Warna', store=True)
    keterangan = fields.Text(string='keterangan', store=True)
    
    brand = fields.Char(string=u'Brand', store=True)
    model_sample = fields.Char(string=u'Model', store=True)
    tipe = fields.Char(string=u'Type', store=True)

    gum_relaxed_x= fields.Float(string='Gum Relaxed x ', store=True)
    gum_relaxed_y= fields.Float(string='Gum Relaxed y ', store=True)

    leg_gum_relaxed_x= fields.Float(string='Leg Gum Relaxed x ', store=True)
    leg_gum_relaxed_y= fields.Float(string='Leg Gum Relaxed y ', store=True)

    leg_gum_atas_relaxed_x= fields.Float(string='Leg Gum Atas Relaxed x ', store=True)
    leg_gum_atas_relaxed_y= fields.Float(string='Leg Gum Atas Relaxed y ', store=True)

    leg_gum_bawah_relaxed_x= fields.Float(string='Leg Gum Bawah Relaxed x ', store=True)
    leg_gum_bawah_relaxed_y= fields.Float(string='Leg Gum Bawah Relaxed y ', store=True)

    leg_relaxed_x= fields.Float(string=' Leg Relaxed x', store=True)
    leg_relaxed_y= fields.Float(string='Leg Relaxed y ', store=True)

    foot_relaxed_x= fields.Float(string=' Foot Relaxed x', store=True)
    foot_relaxed_y= fields.Float(string=' Foot Relaxed y', store=True)

    foot_gum_relaxed_x= fields.Float(string='Foot Gum Relaxed x ', store=True)
    foot_gum_relaxed_y= fields.Float(string='Foot Gum Relaxed y ', store=True)

    hell_relaxed_x= fields.Float(string='Heel Relaxed x ', store=True)
    hell_relaxed_y= fields.Float(string='Heel Relaxed y ', store=True)

    gum_atas_relaxed_x = fields.Float(string='Gum Atas Relaxed X', store=True)
    gum_atas_relaxed_y = fields.Float(string='Gum Atas Relaxed Y', store=True)

    gum_bawah_relaxed_x = fields.Float(string='Gum Bawah relaxed X', store=True)
    gum_bawah_relaxed_y = fields.Float(string='Gum Bawah Relaxed Y' , store=True)

    leg_gum_tengah_relaxed_x = fields.Float(string='Leg Gum Tengah Relaxed X', store=True)
    leg_gum_tengah_relaxed_y = fields.Float(string='Leg Gum Tengah Relaxed Y', store=True)
    
    
    style = fields.Char(string=u'Style', store=True)
    artikel = fields.Char(string=u'Artikel', store=True)
    body = fields.Many2one('product.product',string=u'Body', store=True)
    wording_munich = fields.Many2one('product.product',string=u'Wording', store=True)
    logo = fields.Many2one('product.product',string=u'Logo', store=True)
    hell = fields.Many2one('product.product',string=u'Heel', store=True)
    toe = fields.Many2one('product.product',string=u'Toe', store=True)
    transfer = fields.Many2one('product.product',string=u'Transfer', store=True)
    lintoe = fields.Many2one('product.product',string=u'Lintoe', store=True)
    penjerat = fields.Many2one('product.product',string=u'Penjerat', store=True)
    karet = fields.Many2one('product.product',string=u'Karet', store=True)
    patter_1 = fields.Many2one('product.product',string=u'Pattern 1', store=True)
    patter_2 = fields.Many2one('product.product',string=u'Pattern 2', store=True)
    patter_3 = fields.Many2one('product.product',string=u'Pattern 3', store=True)
    patter_4 = fields.Many2one('product.product',string=u'Pattern 4', store=True)
    patter_5 = fields.Many2one('product.product',string=u'Pattern 5', store=True)
    patter_6 = fields.Many2one('product.product',string=u'Pattern 6', store=True)
    patter_7 = fields.Many2one('product.product',string=u'Pattern 7', store=True)
    patter_8 = fields.Many2one('product.product',string=u'Pattern 8', store=True)
    patter_9 = fields.Many2one('product.product',string=u'Pattern 9', store=True)
    patter_10 = fields.Many2one('product.product',string=u'Pattern 10', store=True)
    jumlah_pasang = fields.Integer(string='Jumlah Pasang', store=True)

    #untuk BOM Benang
    needle = fields.Char(string=u'Needle', store=True)
    nama_sample = fields.Char(string=u'Nama Sample', store=True)