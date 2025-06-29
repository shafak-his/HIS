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


class EmHmsPediatricICU(models.Model):
    _name = 'em.hms.pediatric.icu'
    _description = 'ICU'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'pediatric_icu_medical_history_rel', 'icu_id', 'medical_history_id', string='Medical History')
    mother_age = fields.Integer('Age Of Mother', tracking=True)
    spouses_relationship = fields.Char('Relationship between Spouses', tracking=True)
    child_order = fields.Integer('Child Order With Mother', tracking=True)
    is_neonatal_deaths = fields.Boolean('Is There Neonatal Deaths?', tracking=True)
    is_skeletal_malformations = fields.Boolean('Skeletal Malformations', tracking=True)
    spiritual_motor = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ], string='Spiritual-Motor Development And Disability', tracking=True)
    nutrition_breastfeeding = fields.Selection([
        ('natural', 'Natural'),
        ('artificial', 'Artificial')
    ], string='Nutrition And Breastfeeding', tracking=True)
    mother_blood_group = fields.Selection(BLOOD_TYPES, string='Mother Blood Group', tracking=True)
    child_birth_weight = fields.Float('Birth Weight Of Child', tracking=True)
    child_blood_group = fields.Selection(BLOOD_TYPES, string='Child Blood Group', tracking=True)
    is_child_resuscitation = fields.Boolean('Was Resuscitation Performed For Child?', tracking=True)
    is_previous_admission = fields.Boolean('Is There A Previous Incubator Admission?', tracking=True)
    other_notes = fields.Char('Other notes', tracking=True)
    current_weight = fields.Float('Current Weight (kg)', tracking=True)
    cranial_circumference = fields.Integer('Cranial Circumference', tracking=True)
    devices_general_examination = fields.Char('General Examination Of Devices', tracking=True)
    differential_diagnosis = fields.Char('Differential Diagnosis', tracking=True)
    technician_doctor_id = fields.Many2one('hr.employee', string='Technician Doctor', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('wing', 'Wing'),
        ('death', 'Death'),
        ('referral', 'Referral To Another Hospital')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'icu_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'icu_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'icu_id', string='Image Requests')
    
    observation_ids = fields.One2many('em.hms.daily.observation', 'icu_id', string='Daily Observations')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'icu_id', string='Vital Signs')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'icu_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'icu_id', string='Necessity Giving')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    
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
    

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })