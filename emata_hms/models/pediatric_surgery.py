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


class EmHmsPediatricSurgery(models.Model):
    _name = 'em.hms.pediatric.surgery'
    _description = 'Surgery'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    weight = fields.Float('Weight (kg)', tracking=True)
    case_type = fields.Selection([
        ('cold', 'Cold'),
        ('emergency', 'Emergency')
    ], string='Type Of Case', tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    surgical_procedure_ids = fields.Many2many('em.hms.surgical.procedure', 'pediatric_surgery_surgical_procedure_rel', 'pediatric_surgery_id', 'surgical_procedure_id', string='Surgical Procedure', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'pediatric_surgery_medical_history_rel', 'pediatric_surgery_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'pediatric_surgery_surgical_history_rel', 'pediatric_surgery_id', 'surgical_history_id', string='Surgical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'pediatric_surgery_medication_history_rel', 'pediatric_surgery_id', 'medication_history_id', string='Medication History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'pediatric_surgery_allergic_history_rel', 'pediatric_surgery_id', 'allergic_history_id', string='Allergic History')
    child_blood_group = fields.Selection(BLOOD_TYPES, string='Child Blood Group', tracking=True)
    
    admitting_doctor_id = fields.Many2one('hr.employee', string='Admitting Doctor', tracking=True)
    discharge_doctor_id = fields.Many2one('hr.employee', string='Discharge Doctor', tracking=True)
    admitting_nurse_id = fields.Many2one('hr.employee', string='Admitting Nurse', tracking=True)
    guardian_name = fields.Char('Name Of Patient\'s Guardian', tracking=True)
    anesthesia_report = fields.Char('Anesthesia Report', tracking=True)
    surgical_procedure_report = fields.Char('Surgical Procedure Report', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('care', 'Care'),
        ('death', 'Death'),
        ('referral', 'Referral To Another Hospital')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    analysis_request_ids = fields.One2many('em.hms.analysis.request', 'pediatric_surgery_id', string='Analysis Requests')
    image_request_ids = fields.One2many('em.hms.image.request', 'pediatric_surgery_id', string='Image Requests')
    
    observation_ids = fields.One2many('em.hms.daily.observation', 'pediatric_surgery_id', string='Daily Observations')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'pediatric_surgery_id', string='Vital Signs')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'pediatric_surgery_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'pediatric_surgery_id', string='Necessity Giving')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_admission_datetime',
            'CHECK (admission_datetime <= NOW())',
            'Admission Date/Time Must Not Be Newer Than Now.'
        ),
        (
            'check_graduation_date',
            'CHECK (graduation_date <= CURRENT_DATE)',
            'Graduation Date Must Not Be Newer Than Today.'
        ),
    ]

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.medical_history_ids = [(6, 0, [record.id for record in self.patient_id.medical_history_ids])]
            self.surgical_history_ids = [(6, 0, [record.id for record in self.patient_id.surgical_history_ids])]
            self.medication_history_ids = [(6, 0, [record.id for record in self.patient_id.medication_history_ids])]
            self.allergic_history_ids = [(6, 0, [record.id for record in self.patient_id.allergic_history_ids])]