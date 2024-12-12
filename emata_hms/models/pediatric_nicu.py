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


class EmHmsPediatricNICU(models.Model):
    _name = 'em.hms.pediatric.nicu'
    _description = 'NICU'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    main_complaint = fields.Char('Main Complaint', tracking=True)
    complaint_details = fields.Char('Complaint Details', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    mother_age = fields.Integer('Age Of Mother', tracking=True)
    spouses_relationship = fields.Char('Relationship between Spouses', tracking=True)
    birth_place = fields.Selection([
        ('shafak_hospital', 'Shafak Hospital'),
        ('another_place', 'Another Place')
    ], string='Place Of Birth', tracking=True)
    other_birth_place = fields.Char('Specify Place Of Birth', tracking=True)
    child_order = fields.Integer('Child Order With Mother', tracking=True)
    birth_type = fields.Selection([
        ('normal', 'Normal'),
        ('cesarean_section', 'Cesarean Section')
    ], string='Type Of Birth', tracking=True)
    is_neonatal_deaths = fields.Boolean('Is There Neonatal Deaths?', tracking=True)
    is_miscarriages = fields.Boolean('Is There Miscarriages?', tracking=True)
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
    gestational_weeks_count = fields.Integer('Number Of Gestational Weeks', tracking=True)
    child_birth_weight = fields.Float('Birth Weight Of Child', tracking=True)
    child_blood_group = fields.Selection(BLOOD_TYPES, string='Child Blood Group', tracking=True)
    is_child_resuscitation = fields.Boolean('Was Resuscitation Performed For Child?', tracking=True)
    is_previous_admission = fields.Boolean('Is There A Previous Incubator Admission?', tracking=True)
    first_meconium_after_birth = fields.Integer('First Meconium After Birth (Hour(s))', tracking=True)
    first_urination_after_birth = fields.Integer('First Urination After Birth (Hour(s))', tracking=True)
    other_notes = fields.Char('Other notes', tracking=True)
    current_weight = fields.Float('Current Weight (kg)', tracking=True)
    current_height = fields.Float('Current Height (cm)', tracking=True)
    cranial_circumference = fields.Integer('Cranial Circumference', tracking=True)
    devices_general_examination = fields.Char('General Examination Of Devices', tracking=True)
    newborn_reflexes_examination = fields.Char('Examination Of Newborn Reflexes', tracking=True)
    differential_diagnosis = fields.Char('Differential Diagnosis', tracking=True)
    final_diagnosis = fields.Char('Final Diagnosis At Diagnosis', tracking=True)
    admitting_doctor_id = fields.Many2one('hr.employee', string='Admitting Doctor', tracking=True)
    admitting_nurse_id = fields.Many2one('hr.employee', string='Admitting Nurse', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('incubator', 'Incubator'),
        ('death', 'Death'),
        ('referral', 'Referral To Another Hospital')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'nicu_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'nicu_id', string='Image Requests')
    
    observation_ids = fields.One2many('em.hms.daily.observation', 'nicu_id', string='Daily Observations')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'nicu_id', string='Vital Signs')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'nicu_id', string='Daily Necessities')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'nicu_id', string='Necessity Giving')
    
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

