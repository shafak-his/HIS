from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSGynochologicalClinicVisit(models.Model):
    _name = 'em.hms.rhs.gynochological.clinic.visit'
    _description = 'Gynochological Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', string='Patient Name', required=True, domain=[('is_patient','=',True)], tracking=True)
    clinic_id = fields.Many2one('em.hms.clinic', string='Clinic Name', tracking=True,required=True)
    current_complaint = fields.Char('Current Complaint', tracking=True, required=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True, required=True)
    procedures_followed = fields.Char('Procedures Followed', tracking=True, required=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
    procedure_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('non_emergency', 'Non-Emergency'),
        ('other', 'Other')
    ], string='Type Of Procedure', tracking=True, required=True)
    other_procedure_type = fields.Char('Other Type Of Procedure', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('acceptance', 'Acceptance'),
        ('Referral', 'referral')
    ], string='Graduation To', tracking=True, required=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True, required=True)
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'gynochological_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'gynochological_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'gynochological_visit_id', string='Image Requests')

    medical_history_ids = fields.Many2many('em.hms.medical.history', 'gynochological_visit_medical_history_rel', 'gynochological_visit_id', 'medical_history_id', string='Medical History' ,compute= '_compute_medical_history')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'general_clinic_visit_allergic_history_rel', 'gynochological_visit_visit_id', 'allergic_history_id', string='Allergic History' ,compute= '_compute_allergic_history')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'gynochological_visit_medication_history_rel', 'gynochological_visit_id', 'medication_history_id', string='Medication History',compute= '_compute_medication_history')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'gynochological_visit_surgical_history_rel', 'gynochological_visit_id', 'surgical_history_id', string='Surgical History',compute= '_compute_surgical_history')

    gestational_age = fields.Integer('Gestational Age In Weeks', tracking=True)
    arrival = fields.Selection([
        ('vertical', 'Vertical'),
        ('completely_crippled', 'Completely Crippled'),
        ('incompletely_crippled', 'Incompletely crippled'),
        ('feet', 'Feet'),
        ('cross', 'Cross'),
        ('frontal', 'Frontal'),
        ('facial', 'Facial'),
       ('unknow', 'unknow')
    ], string='Arrival', tracking=True)
    eco_auscultation = fields.Integer('Eco Auscultation', tracking=True)
    eco_auscultation_new =fields.Selection([
        ('negative', 'Negative'),
        ('positive', 'Positive')
      
    ], string='auscultation', tracking=True)

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

    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    notes = fields.Char('Notes', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    
    _sql_constraints = [
        (
            'check_visit_datetime',
            'CHECK (visit_datetime <= NOW())',
            'Visit Date/Time Must Not Be Newer Than Now.'
        ),
    ]

    @api.depends('company_id', 'clinic_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, self.clinic_id, fields.Date.today()).ids

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })


    @api.depends('patient_id')
    def _compute_medical_history(self):
        for rec in self:
           if rec.patient_id:
               
               rec.medical_history_ids = rec.patient_id.medical_history_ids
           else:
              
               rec.medical_history_ids = [(5, 0, 0)]
    @api.depends('patient_id')
    def _compute_allergic_history(self):
        for rec in self:
           if rec.patient_id:
               
               rec.allergic_history_ids = rec.patient_id.allergic_history_ids
           else:
              
               rec.allergic_history_ids = [(5, 0, 0)]
    @api.depends('patient_id')
    def _compute_medication_history(self):
        for rec in self:
           if rec.patient_id:
               
               rec.medication_history_ids = rec.patient_id.medication_history_ids
           else:
              
               rec.medication_history_ids = [(5, 0, 0)]
    @api.depends('patient_id')
    def _compute_surgical_history(self):
        for rec in self:
           if rec.patient_id:
               
               rec.surgical_history_ids = rec.patient_id.surgical_history_ids
           else:
              
               rec.surgical_history_ids = [(5, 0, 0)]