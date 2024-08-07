from odoo import _, api, fields, models, exceptions, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_phc_medication = fields.Boolean('Is PHC Medication')
    is_phc_analysis = fields.Boolean('Is PHC Analysis')
    is_phc_image = fields.Boolean('Is PHC Image')