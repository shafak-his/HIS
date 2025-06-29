from odoo import _, api, fields, models, exceptions, tools

class EmHmsMedicalSign(models.Model):
    _name = 'em.hms.medical.sign'
    _description = 'Medical Sign'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name',  domain=[('is_patient','=',True)])
    
    