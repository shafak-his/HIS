from odoo import _, api, fields, models, exceptions, tools

class EmHmsMedicationHistory(models.Model):
    _name = 'em.hms.medication.history'
    _description = 'Medication History'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name')
    activity_name = fields.Char('Activity Name')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
