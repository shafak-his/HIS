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
    
    birth_datetime = fields.Datetime('Date And Time Of Birth', required=True, tracking=True)
    birth_medication_ids = fields.Many2many('product.template', 'rhs_delivery_product_birth_medication_rel', 'delivery_id', 'product_id', string='Medications Used During Birth', domain="[('is_birth_medication', '=', True)]", required=True)
    birth_report = fields.Char('Birth Report', tracking=True)
    newborn_general_condition = fields.Selection([
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
    
    discharge_datetime = fields.Datetime('Date Of Discharge And Time', required=True, tracking=True)
    discharge_supervising_physician_id = fields.Many2one('hr.employee', string='Supervising Physician', required=True)
    discharge_duty_midwife_id = fields.Many2one('hr.employee', string='Midwife On Duty', required=True)
    patient_condition = fields.Selection([
        ('to_home', 'To Home'),
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
    
    labor_ids = fields.One2many('em.hms.rhs.delivery.labor', 'delivery_id', string='Labor Monitoring')
    labors_count = fields.Integer(compute='_compute_labors_count', string='Labors Count')
    vital_signs_ids = fields.One2many('em.hms.vital.signs', 'delivery_id', string='Vital Signs Monitoring')
    vital_signs_count = fields.Integer(compute='_compute_vital_signs_count', string='Vital Signs Reports')
    post_birth_ids = fields.One2many('em.hms.rhs.delivery.post.birth', 'delivery_id', string='Post-Birth Monitoring')
    post_births_count = fields.Integer(compute='_compute_post_births_count', string='Post-Birth Reports')

    @api.depends('labor_ids')
    def _compute_labors_count(self):
        for record in self:
            record.labors_count = len(record.labor_ids)
            
    @api.depends('vital_signs_ids')
    def _compute_vital_signs_count(self):
        for record in self:
            record.vital_signs_count = len(record.vital_signs_ids)
            
    @api.depends('post_birth_ids')
    def _compute_post_births_count(self):
        for record in self:
            record.post_births_count = len(record.post_birth_ids)
            
            
    def action_get_delivery_labors_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Labor Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.delivery.labor',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_delivery_vital_signss_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vital Signs Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.vital.signs',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_delivery_post_births_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Post-Birth Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.delivery.post.birth',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }

