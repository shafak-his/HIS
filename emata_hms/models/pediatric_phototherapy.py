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


class EmHmsPediatricPhototherapy(models.Model):
    _name = 'em.hms.pediatric.phototherapy'
    _description = 'Phototherapy'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date', required=True, tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    mother_age = fields.Integer('Age Of Mother', tracking=True)
    spouses_relationship = fields.Char('Relationship between Spouses', tracking=True)
    childbirth_pregnancy_conditions = fields.Char('Conditions Of Pregnancy And Childbirth', tracking=True)
    family_history = fields.Char('The Family History', tracking=True)
    is_neonatal_deaths = fields.Boolean('Is There Neonatal Deaths?', tracking=True)
    is_miscarriages = fields.Boolean('Is There Miscarriages?', tracking=True)
    nutrition_breastfeeding = fields.Selection([
        ('natural', 'Natural'),
        ('artificial', 'Artificial')
    ], string='Nutrition And Breastfeeding', tracking=True)
    mother_blood_group = fields.Selection(BLOOD_TYPES, string='Mother Blood Group', tracking=True)
    child_blood_group = fields.Selection(BLOOD_TYPES, string='Child Blood Group', tracking=True)
    other_notes = fields.Char('Other notes', tracking=True)
    clinical_general_examination = fields.Char('Clinical/General Examination', tracking=True)
    newborn_reflexes_examination = fields.Char('Examination Of Newborn Reflexes', tracking=True)
    clinical_followup = fields.Char('Clinical Follow-up', tracking=True)
    final_diagnosis = fields.Char('Final Diagnosis', tracking=True)
    pre_graduation_examination = fields.Char('Pre-Graduation Examination', tracking=True)
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
    
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'phototherapy_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'phototherapy_id', string='Image Requests')
    
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'phototherapy_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'phototherapy_id', string='Necessity Giving')
    
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

