from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDelivery(models.Model):
    _name = 'em.hms.rhs.delivery'
    _description = 'Normal Delivery'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_date = fields.Date('Date Of Admission', required=True, tracking=True)
    admitting_midwife_id = fields.Many2one('hr.employee', string='Name Of Admitting Midwife')
    admitting_physician_id = fields.Many2one('hr.employee', string='Name Of Admitting Physician')
    husband_name = fields.Char('Name Of Husband', tracking=True)
    guardian_name = fields.Char('Name Of Patient\'s Guardian', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'delivery_medical_history_rel', 'delivery_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'delivery_surgical_history_rel', 'delivery_id', 'surgical_history_id', string='Surgical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'delivery_medication_history_rel', 'delivery_id', 'medication_history_id', string='Drug History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'delivery_allergic_history_rel', 'delivery_id', 'allergic_history_id', string='Allergic History')
    initial_diagnosis = fields.Char('Initial Diagnosis', tracking=True)
    child_name = fields.Char('Name Of Child', tracking=True)
    
    natural_births_count = fields.Integer('# Natural Births', tracking=True)
    cesarean_births_count = fields.Integer('# Cesarean Births', tracking=True)
    miscarriages_count = fields.Integer('# Miscarriages', tracking=True)
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
    ], string='Pregnancy-Related Diseases In Previous Pregnancies', tracking=True)
    
    gestational_age = fields.Integer('Gestational Age In Weeks', tracking=True)
    arrival = fields.Selection([
        ('vertical', 'Vertical'),
        ('completely_crippled', 'Completely Crippled'),
        ('incompletely_crippled', 'Incompletely crippled'),
        ('feet', 'Feet'),
        ('cross', 'Cross'),
        ('frontal', 'Frontal'),
        ('facial', 'Facial')
    ], string='Arrival', tracking=True)
    eco_auscultation = fields.Integer('Eco Auscultation', tracking=True)
    placenta = fields.Selection([
        ('bottomless', 'Bottomless'),
        ('low', 'Low'),
        ('marginal', 'Marginal'),
        ('central', 'Central'),
        ('front', 'Front')
    ], string='Placenta', tracking=True)
    amniotic_fluid = fields.Selection([
        ('good', 'Good'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus')
    ], string='Amniotic Fluid', tracking=True)
    
    birth_datetime = fields.Datetime('Date And Time Of Birth', tracking=True)
    birth_medication_ids = fields.Many2many('product.template', 'rhs_delivery_product_birth_medication_rel', 'delivery_id', 'product_id', string='Medications Used During Birth', domain="[('is_birth_medication', '=', True)]")
    birth_report = fields.Char('Birth Report', tracking=True)
    newborn_general_condition = fields.Selection([
        ('good_vitality', 'Good Vitality'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deceased', 'Deceased')
    ], string='General Condition Of The Child', tracking=True)
    newborn_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender Of The Newborn', tracking=True)
    newborn_weight = fields.Float('Weight Of The Newborn', tracking=True)
    is_breastfeeding_first_hour = fields.Boolean('Breastfeeding Within The First Hour', tracking=True)
    
    discharge_datetime = fields.Datetime('Date Of Discharge And Time', tracking=True)
    discharge_supervising_physician_id = fields.Many2one('hr.employee', string='Supervising Physician')
    discharge_duty_midwife_id = fields.Many2one('hr.employee', string='Midwife On Duty')
    patient_condition = fields.Selection([
        ('to_home', 'To Home'),
        ('another_hospital', 'Another Hospital'),
        ('other', 'Other')
    ], string='Patient''s Condition', tracking=True)
    newborn_condition = fields.Selection([
        ('to_home', 'To Home'),
        ('another_hospital', 'Another Hospital'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deceased', 'Deceased')
    ], string='Newborn''s Condition', tracking=True)
    patient_companion_name = fields.Char('Patient''s Companion''s Name', tracking=True)
    patient_companion_relationship = fields.Char('Relationship', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    labor_ids = fields.One2many('em.hms.labor', 'delivery_id', string='Labor Monitoring')
    labors_count = fields.Integer(compute='_compute_labors_count', string='Labors Count')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'delivery_id', string='Vital Signs Monitoring')
    vital_signs_count = fields.Integer(compute='_compute_vital_signs_count', string='Vital Signs Reports')
    post_birth_ids = fields.One2many('em.hms.post.surgery', 'delivery_id', string='Post-Birth Monitoring')
    post_births_count = fields.Integer(compute='_compute_post_births_count', string='Post-Birth Reports')

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.medical_history_ids = [(6, 0, [record.id for record in self.patient_id.medical_history_ids])]
            self.surgical_history_ids = [(6, 0, [record.id for record in self.patient_id.surgical_history_ids])]
            self.medication_history_ids = [(6, 0, [record.id for record in self.patient_id.medication_history_ids])]
            self.allergic_history_ids = [(6, 0, [record.id for record in self.patient_id.allergic_history_ids])]

    @api.depends('labor_ids')
    def _compute_labors_count(self):
        for record in self:
            record.labors_count = len(record.labor_ids)
            
    @api.depends('vital_sign_ids')
    def _compute_vital_signs_count(self):
        for record in self:
            record.vital_signs_count = len(record.vital_sign_ids)
            
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
            'res_model': 'em.hms.labor',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_delivery_vital_signs_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vital Signs Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.vital.sign',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_delivery_post_births_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Post-Birth Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.post.surgery',
            'domain': [('delivery_id', '=', self.id)],
            'context': "{'create': False}"
        }

