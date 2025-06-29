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

class EmHmsRHSANCVisit(models.Model):
    _name = 'em.hms.rhs.anc.visit'
    _description = 'ANC Visit'
    _rec_name = 'anc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    anc_id = fields.Many2one('em.hms.rhs.anc', string='ANC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='anc_id.patient_id')
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    medical_signs_ids =fields.Many2many('em.hms.medical.sign', 'rhs_anc_medicals_sign_rel', 'anc_id', 'medical_signs_id', string='Medical Signs')
    arterial_pressure = fields.Float('Arterial Pressure In Sitting Position', tracking=True)
    weight = fields.Float('Weight', tracking=True)
    pulse_rate = fields.Float('Pulse Heart Rate (n/d)', tracking=True)
    mother_pressure = fields.Char('Arterial Pressure In Sitting Position', tracking=True ,default='0/0')
    main_complaint = fields.Char('Main Complaint During This Visit', tracking=True)
    head_diameter = fields.Float('Measurement Of Head Diameter', tracking=True)
    thigh_length = fields.Float('Thigh Length', tracking=True)
    presence = fields.Selection([
        ('vertical', 'Vertical'),
        ('completely_crippled', 'Completely Crippled'),
        ('incompletely_crippled', 'Incompletely crippled'),
        ('feet', 'Feet'),
        ('cross', 'Cross'),
        ('frontal', 'Frontal'),
        ('facial', 'Facial')
    ], string='Presence', tracking=True)
    fluid = fields.Selection([
        ('good', 'Good'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus')
    ], string='Fluid', tracking=True)
    deformities = fields.Char('Deformities', tracking=True)
    child_blood_group = fields.Selection(BLOOD_TYPES, string='Child Blood Group', tracking=True)
    child_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Child Gender', tracking=True)
    genital_age_in_weeks = fields.Integer('Genital Age In Weeks', tracking=True)
    gestational_age_according_to_crl=fields.Integer('Genital Age according to CRL', tracking=True)
    gestational_age_according_to_gs=fields.Integer('Genital Age according to GS', tracking=True)
    vaginal_examination = fields.Selection([
        ('done', 'Done'),
        ('not_done', 'Not Done'),
        ('patient_refused', 'Patient Refused')
    ], string='Vaginal Examination If Performed', tracking=True)
    placenta = fields.Selection([
        ('bottomless', 'Bottomless'),
        ('low', 'Low'),
        ('marginal', 'Marginal'),
        ('central', 'Central'),
        ('front', 'Front')
    ], string='Placenta', tracking=True)
    if_done_explain = fields.Char('If Done Explain', tracking=True)
    treatment = fields.Char('Treatment', tracking=True)
    is_tetanus_vaccined = fields.Boolean('Has The Patient Received The Tetanus Vaccine?', tracking=True)
    next_visit_date = fields.Date('Date Of Next Visit', tracking=True)
    examiner_name = fields.Char('Name Of Examiner', tracking=True)
    additional_notes = fields.Char('Additional Notes', tracking=True)
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'anc_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'anc_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'anc_visit_id', string='Image Requests')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
