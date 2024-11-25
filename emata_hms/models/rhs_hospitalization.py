from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSHospitalization(models.Model):
    _name = 'em.hms.rhs.hospitalization'
    _description = 'Hospitalization'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_date = fields.Date('Date Of Admission', required=True, tracking=True)
    admitting_midwife_id = fields.Many2one('hr.employee', string='Name Of Admitting Midwife')
    admitting_physician_id = fields.Many2one('hr.employee', string='Name Of Admitting Physician')
    husband_name = fields.Char('Name Of Husband', tracking=True)
    guardian_name = fields.Char('Name Of Patient\'s Guardian', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'hospitalization_medical_history_rel', 'hospitalization_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'hospitalization_surgical_history_rel', 'hospitalization_id', 'surgical_history_id', string='Surgical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'hospitalization_medication_history_rel', 'hospitalization_id', 'medication_history_id', string='Drug History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'hospitalization_allergic_history_rel', 'hospitalization_id', 'allergic_history_id', string='Allergic History')
    current_diagnosis = fields.Char('Current Diagnosis', tracking=True)
    
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
    other_findings = fields.Char('Other Findings', tracking=True)
    
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
    
    medication_request_ids = fields.One2many('em.hms.medication.request', 'hospitalization_id', string='Medication Requests')
    analysis_request_ids = fields.One2many('em.hms.analysis.request', 'hospitalization_id', string='Analysis Requests')

    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'hospitalization_id', string='Vital Signs Monitoring')
    vital_signs_count = fields.Integer(compute='_compute_vital_signs_count', string='Vital Signs Reports')
    labor_ids = fields.One2many('em.hms.labor', 'hospitalization_id', string='Labor Monitoring')
    labors_count = fields.Integer(compute='_compute_labors_count', string='Labors Count')
    monitoring_ids = fields.One2many('em.hms.rhs.hospitalization.monitoring', 'hospitalization_id', string='Monitoring')
    monitorings_count = fields.Integer(compute='_compute_monitorings_count', string='Monitorings Count')
    necessity_ids = fields.One2many('em.hms.daily.necessity', 'hospitalization_id', string='Daily Necessity')
    necessities_count = fields.Integer(compute='_compute_necessities_count', string='Daily Necessity Count')
    commitment_ids = fields.One2many('em.hms.necessity.giving', 'hospitalization_id', string='Necessity Giving')
    commitments_count = fields.Integer(compute='_compute_commitments_count', string='Necessity Giving Count')
    
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.medical_history_ids = [(6, 0, [record.id for record in self.patient_id.medical_history_ids])]
            self.surgical_history_ids = [(6, 0, [record.id for record in self.patient_id.surgical_history_ids])]
            self.medication_history_ids = [(6, 0, [record.id for record in self.patient_id.medication_history_ids])]
            self.allergic_history_ids = [(6, 0, [record.id for record in self.patient_id.allergic_history_ids])]
    
    @api.depends('vital_sign_ids')
    def _compute_vital_signs_count(self):
        for record in self:
            record.vital_signs_count = len(record.vital_sign_ids)
            
    @api.depends('labor_ids')
    def _compute_labors_count(self):
        for record in self:
            record.labors_count = len(record.labor_ids)
            
    @api.depends('monitoring_ids')
    def _compute_monitorings_count(self):
        for record in self:
            record.monitorings_count = len(record.monitoring_ids)
            
    @api.depends('necessity_ids')
    def _compute_necessities_count(self):
        for record in self:
            record.necessities_count = len(record.necessity_ids)
    
    @api.depends('commitment_ids')
    def _compute_commitments_count(self):
        for record in self:
            record.commitments_count = len(record.commitment_ids)
            
    def action_get_hospitalization_labors_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Labor Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.hospitalization.labor',
            'domain': [('hospitalization_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_hospitalization_vital_signs_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vital Signs Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.vital.sign',
            'domain': [('hospitalization_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    def action_get_hospitalization_monitorings_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Post-Birth Monitoring',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.hospitalization.monitoring',
            'domain': [('hospitalization_id', '=', self.id)],
            'context': "{'create': False}"
        }

