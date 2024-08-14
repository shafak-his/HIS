from odoo import _, api, fields, models, exceptions, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_medication = fields.Boolean('Is Medication')
    is_medical_analysis = fields.Boolean('Is Medical Analysis')
    is_medical_imaging = fields.Boolean('Is Medical Imaging')