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


class EmHmsPediatricSurgeryClinic(models.Model):
    _name = 'em.hms.pediatric.surgery.clinic'
    _description = 'Surgery Clinic'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    weight = fields.Float('Weight (kg)', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    oxygen = fields.Float('Oxygen', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    case_type = fields.Selection([
        ('cold', 'Cold'),
        ('emergency', 'Emergency')
    ], string='Type Of Case', tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'pediatric_surgery_clinic_medical_history_rel', 'surgery_clinic_id', 'medical_history_id', string='Medical History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'pediatric_surgery_clinic_allergic_history_rel', 'surgery_clinic_id', 'allergic_history_id', string='Allergic History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'pediatric_surgery_clinic_medication_history_rel', 'surgery_clinic_id', 'medication_history_id', string='Medication History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'pediatric_surgery_clinic_surgical_history_rel', 'surgery_clinic_id', 'surgical_history_id', string='Surgical History')
    
    graduation_to = fields.Selection([
        ('surgery', 'Surgery'),
        ('wing', 'Wing'),
        ('care', 'Care'),
        ('home', 'Home'),
        ('referral', 'Referral To Another Hospital')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    consultations = fields.Char('Consultations', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'pediatric_surgery_clinic_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'pediatric_surgery_clinic_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'pediatric_surgery_clinic_id', string='Image Requests')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    allowed_project_ids = fields.Many2many('project.project', compute='_compute_allowed_project_ids', string='Allowed Projects', compute_sudo=True)
    
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

    @api.onchange('allowed_project_ids')
    def _onchange_allowed_project_ids(self):
        if self.allowed_project_ids:
            self.project_id = self.allowed_project_ids[0].id

    @api.depends('company_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, False, fields.Date.today()).ids

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.medical_history_ids = [(6, 0, [record.id for record in self.patient_id.medical_history_ids])]
            self.surgical_history_ids = [(6, 0, [record.id for record in self.patient_id.surgical_history_ids])]
            self.medication_history_ids = [(6, 0, [record.id for record in self.patient_id.medication_history_ids])]
            self.allergic_history_ids = [(6, 0, [record.id for record in self.patient_id.allergic_history_ids])]

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })