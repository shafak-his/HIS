from odoo import _, api, fields, models, exceptions, tools


class EmHmsDialKidneyHistory(models.Model):
    _name = 'em.hms.dial.kidney.history'
    _description = 'Kidney History'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    cause_ckd = fields.Selection([
        ('diabetes', 'Diabetes'),
        ('high_blood_pressure', 'High blood pressure'),
        ('glomerulonephritis', 'Glomerulonephritis'),
        ('cystic_kidney', 'Cystic kidney disease'),
        ('other_causes', 'Other causes'),
        ('unknown', 'Unknown')
    ], string='Cause of chronic kidney disease', tracking=True)
    previous_treatment_ckd = fields.Char('Previous treatment for CKD', tracking=True)
    dialysis_start_date = fields.Date('Dialysis start date', tracking=True)
    diagnostic_procedures_ckd = fields.Selection([
        ('lab_tests', 'Laboratory Tests'),
        ('radiological', 'Radiological Investigations'),
        ('kidney_biopsy', 'Kidney Biopsy'),
    ], string='Diagnostic procedures for chronic kidney disease', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
