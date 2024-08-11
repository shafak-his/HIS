from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDelvery(models.Model):
    _name = 'em.hms.rhs.delvery'
    _description = 'RH Service - Normal Delvery'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
    admission_date = fields.Date('Date of admission', required=True, tracking=True)
    admitting_midwife_id = fields.Many2one('hr.employee', string='Name of admitting midwife', required=True, tracking=True)
    admitting_physician_id = fields.Many2one('hr.employee', string='Name of admitting physician', required=True, tracking=True)
    husband_name = fields.Char('Name of husband', required=True)
    guardian_name = fields.Char('Name of patient''s guardian', required=True)
    allergic_history = fields.Char('Allergic History')
    drug_history = fields.Char('Drug History')
    surgical_history = fields.Char('Surgical History')
    medical_history = fields.Char('Medical History')
    initial_diagnosis = fields.Char('Initial diagnosis')
    child_name = fields.Char('Name of child', required=True)
    
    pre_birth_pressure = fields.Char('Pressure', required=True)
    pre_birth_pulse = fields.Integer('Pulse', required=True)
    pre_birth_temperature = fields.Float('Temperature', required=True)
    pre_birth_awareness = fields.Char('Awareness')
    
    number_of_natural_births = fields.Integer('Number of natural births', required=True)
    number_of_cesarean_births = fields.Integer('Number of cesarean births', required=True)
    number_of_miscarriages = fields.Integer('Number of miscarriages', required=True)
    pregnancy_related_diseases = fields.Selection([
        ('gestational', 'Gestational'),
        ('gestational_diabetes', 'Gestational Diabetes'),
        ('pre_shock', 'Pre-shock'),
        ('shaking', 'Shaking'),
        ('group_dissonance', 'Group dissonance'),
        ('hellp', 'HELLP'),
        ('thrombophlebitis', 'Thrombophlebitis'),
        ('other', 'Other diseases'),
        ('none', 'None')
    ], string='Pregnancy-related diseases in previous pregnancies', required=True)
    
    gestational_age = fields.Integer('Gestational age in weeks', required=True)
    arrival = fields.Selection([
        ('vertical', 'Vertical'),
        ('completely_crippled', 'Completely crippled'),
        ('incompletely_crippled', 'Incompletely crippled'),
        ('feet', 'Feet'),
        ('cross', 'Cross'),
        ('frontal', 'Frontal'),
        ('facial', 'Facial')
    ], string='Arrival', required=True, tracking=True)
    eco_auscultation = fields.Integer('Eco Auscultation', required=True)
    placenta = fields.Selection([
        ('bottomless', 'Bottomless'),
        ('low', 'Low'),
        ('marginal', 'Marginal'),
        ('central', 'Central'),
        ('front', 'Front')
    ], string='Placenta', required=True, tracking=True)
    amniotic_fluid = fields.Selection([
        ('good', 'Good'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic hydrocephalus')
    ], string='Amniotic fluid', required=True, tracking=True)
    
    travail_hour = fields.Datetime('Hour', required=True)
    contraction_duration = fields.Integer('Contraction duration', required=True)
    interval_between_contractions = fields.Integer('Interval between contractions', required=True)
    travail_auscultation = fields.Char('Travail Auscultation', required=True)
    dilation = fields.Integer('Dilation', required=True)
    erasure = fields.Integer('Erasure', required=True)
    
    birth_datetime = fields.Datetime('Date and time of birth', required=True)
    medications_birth = fields.Selection([
        ('oxytocin', 'Oxytocin'),
        ('Cytotec', 'Cytotec'),
        ('mitergine', 'Mitergine'),
        ('catalar', 'Catalar'),
        ('propofol', 'Propofol'),
        ('midazolam', 'Midazolam')
    ], string='Medications used during birth', required=True, tracking=True)
    birth_report = fields.Char('Birth Report')
    newborn_condition = fields.Selection([
        ('good_vitality', 'Good vitality'),
        ('transfer_to_care', 'Transfer to care'),
        ('transfer_to_incubators', 'Transfer to incubators'),
        ('deceased', 'Deceased')
    ], string='General condition of the child', required=True, tracking=True)
    newborn_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender of the newborn', required=True, tracking=True)
    newborn_weight = fields.Float('Weight of the newborn', required=True)
    is_breastfeeding_first_hour = fields.Boolean('Breastfeeding within the first hour')
    
    post_birth_datetime = fields.Datetime('Time', required=True)
    post_birth_pressure = fields.Integer('Pressure', required=True)
    post_birth_pulse = fields.Integer('Pulse', required=True)
    post_birth_temperature = fields.Float('Temperature', required=True)
    is_post_birth_safety_ball = fields.Boolean('Safety Ball')
    is_post_birth_urine_voiding = fields.Boolean('Urine Voiding')
    post_birth_notes = fields.Char('Notes')
    
    discharge_datetime = fields.Datetime('Date of discharge and time', required=True)
    discharge_supervising_physician_id = fields.Many2one('hr.employee', string='Supervising physician', required=True, tracking=True)
    discharge_duty_midwife_id = fields.Many2one('hr.employee', string='Midwife on duty', required=True, tracking=True)
    patient_condition = fields.Selection([
        ('to_home', 'To home'),
        ('another_hospital', 'Another hospital'),
        ('other', 'Other')
    ], string='Patient''s condition', required=True, tracking=True)
    newborn_condition = fields.Selection([
        ('to_home', 'To home'),
        ('another_hospital', 'Another hospital'),
        ('transfer_to_care', 'Transfer to care'),
        ('transfer_to_incubators', 'Transfer to incubators'),
        ('deceased', 'Deceased')
    ], string='Newborn''s condition', required=True, tracking=True)
    patient_companion_name = fields.Char('Patient''s companion''s name')
    patient_companion_relationship = fields.Char('Relationship')
    