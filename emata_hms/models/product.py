from odoo import _, api, fields, models, exceptions, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_medication = fields.Boolean('Is Medication')
    is_medical_analysis = fields.Boolean('Is Medical Analysis')
    is_medical_imaging = fields.Boolean('Is Medical Imaging')
    is_birth_medication = fields.Boolean('Is Medication During Birth')
    is_surgery_medication = fields.Boolean('Is Medication During Surgery')