from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDelivery(models.Model):
    _name = 'em.hms.rhs.delivery'
    _description = 'RH Service - Normal Delivery'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True)
    admission_date = fields.Date('Date Of Admission', required=True, tracking=True)
    admitting_midwife_id = fields.Many2one('hr.employee', string='Name Of Admitting Midwife', required=True)
    admitting_physician_id = fields.Many2one('hr.employee', string='Name Of Admitting Physician', required=True)
    husband_name = fields.Char('Name Of Husband', required=True, tracking=True)
    guardian_name = fields.Char('Name Of Patient\'s Guardian', required=True, tracking=True)
    allergic_history = fields.Char('Allergic History', tracking=True)
    drug_history = fields.Char('Drug History', tracking=True)
    surgical_history = fields.Char('Surgical History', tracking=True)
    medical_history = fields.Char('Medical History', tracking=True)
    initial_diagnosis = fields.Char('Initial Diagnosis', tracking=True)
    child_name = fields.Char('Name Of Child', required=True, tracking=True)
    
    pre_birth_pressure = fields.Float('Pressure', required=True, tracking=True)
    pre_birth_pulse = fields.Float('Pulse', required=True, tracking=True)
    pre_birth_temperature = fields.Float('Temperature', required=True, tracking=True)
    pre_birth_awareness = fields.Char('Awareness')
    
    natural_births_count = fields.Integer('Number Of Natural Births', required=True, tracking=True)
    cesarean_births_count = fields.Integer('Number Of Cesarean Births', required=True, tracking=True)
    miscarriages_count = fields.Integer('Number Of Miscarriages', required=True, tracking=True)
    pregnancy_related_diseases = fields.Selection([
        ('gestational', 'Gestational'),
        ('gestational_diabetes', 'Gestational Diabetes'),
        ('pre_shock', 'Pre-Shock'),
        ('shaking', 'Shaking'),
        ('group_dissonance', 'Group Dissonance'),
        ('hellp', 'HELLP'),
        ('thrombophlebitis', 'Thrombophlebitis'),
        ('other', 'Other Diseases'),
        ('none', 'None')
    ], string='Pregnancy-Related Diseases In Previous Pregnancies', required=True, tracking=True)
    
    gestational_age = fields.Integer('Gestational Age In Weeks', required=True, tracking=True)
    arrival = fields.Selection([
        ('vertical', 'Vertical'),
        ('completely_crippled', 'Completely Crippled'),
        ('incompletely_crippled', 'Incompletely crippled'),
        ('feet', 'Feet'),
        ('cross', 'Cross'),
        ('frontal', 'Frontal'),
        ('facial', 'Facial')
    ], string='Arrival', required=True, tracking=True)
    eco_auscultation = fields.Integer('Eco Auscultation', required=True, tracking=True)
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
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus')
    ], string='Amniotic Fluid', required=True, tracking=True)
    
    travail_hour = fields.Datetime('Hour', required=True, tracking=True)
    contraction_duration = fields.Float('Contraction Duration', required=True, tracking=True)
    interval_between_contractions = fields.Float('Interval Between Contractions', required=True, tracking=True)
    travail_auscultation = fields.Char('Travail Auscultation', required=True, tracking=True)
    dilation = fields.Float('Dilation', required=True, tracking=True)
    erasure = fields.Float('Erasure', required=True, tracking=True)
    
    birth_datetime = fields.Datetime('Date And Time Of Birth', required=True, tracking=True)
    medications_birth = fields.Selection([
        ('oxytocin', 'Oxytocin'),
        ('Cytotec', 'Cytotec'),
        ('mitergine', 'Mitergine'),
        ('catalar', 'Catalar'),
        ('propofol', 'Propofol'),
        ('midazolam', 'Midazolam')
    ], string='Medications Used During Birth', required=True, tracking=True)
    birth_report = fields.Char('Birth Report', tracking=True)
    newborn_condition = fields.Selection([
        ('good_vitality', 'Good Vitality'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deceased', 'Deceased')
    ], string='General Condition Of The Child', required=True, tracking=True)
    newborn_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender Of The Newborn', required=True, tracking=True)
    newborn_weight = fields.Float('Weight Of The Newborn', required=True, tracking=True)
    is_breastfeeding_first_hour = fields.Boolean('Breastfeeding Within The First Hour', tracking=True)
    
    post_birth_datetime = fields.Datetime('Time', required=True, tracking=True)
    post_birth_pressure = fields.Integer('Pressure', required=True, tracking=True)
    post_birth_pulse = fields.Integer('Pulse', required=True, tracking=True)
    post_birth_temperature = fields.Float('Temperature', required=True, tracking=True)
    is_post_birth_safety_ball = fields.Boolean('Safety Ball', tracking=True)
    is_post_birth_urine_voiding = fields.Boolean('Urine Voiding', tracking=True)
    post_birth_notes = fields.Char('Notes')
    
    discharge_datetime = fields.Datetime('Date Of Discharge And Time', required=True, tracking=True)
    discharge_supervising_physician_id = fields.Many2one('hr.employee', string='Supervising Physician', required=True)
    discharge_duty_midwife_id = fields.Many2one('hr.employee', string='Midwife On Duty', required=True)
    patient_condition = fields.Selection([
        ('to_home', 'To home'),
        ('another_hospital', 'Another Hospital'),
        ('other', 'Other')
    ], string='Patient''s Condition', required=True, tracking=True)
    newborn_condition = fields.Selection([
        ('to_home', 'To Home'),
        ('another_hospital', 'Another Hospital'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deceased', 'Deceased')
    ], string='Newborn''s Condition', required=True, tracking=True)
    patient_companion_name = fields.Char('Patient''s Companion''s Name', tracking=True)
    patient_companion_relationship = fields.Char('Relationship', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)