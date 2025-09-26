from odoo import _, api, fields, models, exceptions, tools

class EmHmsMedicalHistory(models.Model):
    _name = 'em.hms.medical.history'
    _description = 'Medical History'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])