{
	"name": "marel_in_samlpe_dev_2",
	"version": "1.0", 
	"depends": ["product","marel_in_work_order","mrp","stock",'hr'],
	"author": "asrent345@gmail.com & hendrikus165@gmail.com", 
	"category": "Education", 
	'website': 'http://www.vitraining.com',
	"description": """\

Manage
======================================================================

* this is my academic information system module
* created menu:
* created object
* created views
* logic:

""",
	"data": [
        # "security/ir.model.access.csv",
		"view/menu_2.xml",
		"view/marel_in_samlpe_dev_2.xml",		
		"view/operator_marelinsamlpe_dev2_list.xml",		
		"view/ir_sequence.xml",
		"view/marel_in_bom.xml",
		"view/marelin_permintaan_develop.xml",
		# "view/view_bordir.xml",
		# "view/bom_report_act.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}