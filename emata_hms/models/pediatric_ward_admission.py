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


class EmHmsPediatricWardAdmission(models.Model):
    _name = 'em.hms.pediatric.ward.admission'
    _description = 'Ward Admission'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    pregnancy_childbirth = fields.Char('Pregnancy And Childbirth', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'ward_admission_medical_history_rel', 'ward_admission_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'ward_admission_surgical_history_rel', 'wardt_admission_id', 'surgical_history_id', string='Surgical History')
    family_history = fields.Char('The Family History', tracking=True)
    nutrition = fields.Char('Nutrition', tracking=True)
    vaccines = fields.Char('Vaccines', tracking=True)
    
    
    weight = fields.Float('Weight (kg)', tracking=True)
    height = fields.Float('Height (cm)', tracking=True)
    cranial_circumference = fields.Integer('Cranial Circumference', tracking=True)
    admitting_doctor_id = fields.Many2one('hr.employee', string='Admitting Doctor', tracking=True)
    admitting_nurse_id = fields.Many2one('hr.employee', string='Admitting Nurse', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('care', 'Care'),
        ('death', 'Death'),
        ('referral', 'Referral To Another Hospital')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    consultations = fields.Char('Consultations', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'ward_admission_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'ward_admission_id', string='Image Requests')
    
    observation_ids = fields.One2many('em.hms.daily.observation', 'ward_admission_id', string='Daily Observations')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'ward_admission_id', string='Vital Signs')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'ward_admission_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'ward_admission_id', string='Necessity Giving')
    
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