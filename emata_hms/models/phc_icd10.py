from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcICD10(models.Model):
    _name = 'em.hms.phc.icd10'
    _description = 'PHC ICD10'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Datetime('Diagnosis name', required=True)
    name_lang = fields.Datetime('Diagnosis Arabic name', required=True)
    code = fields.Datetime('Code', required=True)
    is_ncd = fields.Boolean('Is NCD')
    is_traumatic = fields.Boolean('Is Traumatic')
    is_diabetes = fields.Boolean('Is Diabetes')
    
