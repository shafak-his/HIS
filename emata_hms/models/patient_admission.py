from odoo import _, api, fields, models, exceptions, tools

BLOOD_TYPES = [
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O-', 'O-'),
    ('AB-', 'AB-')
]


class EmHmsPatientAdmission(models.Model):
    _name = 'em.hms.patient.admission'
    _description = 'Patient Admission'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    visit_date = fields.Date('Visit Date', required=True, tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    ward_nurse_id = fields.Many2one('hr.employee', string='Name Of The Ward Nurse', tracking=True)
    admission_type = fields.Selection([
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent')
    ], string='Type Of Admission', tracking=True)
    blood_group = fields.Selection(BLOOD_TYPES, string='Blood Group', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    respiratory_rate = fields.Float('Respiratory Rate', tracking=True)
    
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'patient_admission_medical_history_rel', 'patient_admission_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'patient_admission_surgical_history_rel', 'patient_admission_id', 'surgical_history_id', string='Surgical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'patient_admission_medication_history_rel', 'patient_admission_id', 'medication_history_id', string='Medication History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'patient_admission_allergic_history_rel', 'patient_admission_id', 'allergic_history_id', string='Allergic History')
    
    clinic_examination = fields.Char('Clinical Examination', tracking=True)
    complaint_details = fields.Char('Details Of The Medical Complaint', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    
    medication_request_ids = fields.One2many('em.hms.medication.request', 'patient_admission_id', string='Medication Requests')
    analysis_request_ids = fields.One2many('em.hms.analysis.request', 'patient_admission_id', string='Analysis Requests')
    image_request_ids = fields.One2many('em.hms.image.request', 'patient_admission_id', string='Image Requests')
    
    notes = fields.Char('Notes', tracking=True)
    
    surgery_ids = fields.One2many('em.hms.patient.admission.surgery', 'patient_admission_id', string='Surgeries')
    visit_ids = fields.One2many('em.hms.patient.admission.visit', 'patient_admission_id', string='Doctor Visits')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'patient_admission_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'patient_admission_id', string='Necessity Giving')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_visit_date',
            'CHECK (visit_date <= CURRENT_DATE)',
            'Visit Date Must Not Be Newer Than Today.'
        ),
    ]

