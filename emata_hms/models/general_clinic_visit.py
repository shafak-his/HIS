from odoo import _, api, fields, models, exceptions, tools


class EmHmsGeneralClinicVisit(models.Model):
    _name = 'em.hms.general.clinic.visit'
    _description = 'General Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', string='Patient Name', required=True, domain=[('is_patient','=',True)], tracking=True)
    clinic_id = fields.Many2one('em.hms.clinic', string='Clinic Name', tracking=True)
    is_pregnant = fields.Boolean('Is Pregnant?', tracking=True)
    is_lactating = fields.Boolean('Is Lactating?', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    pressure_new = fields.Char('Pressure', tracking=True ,default='0/0')
    weight = fields.Float('Weight (KG)', tracking=True)
    height = fields.Float('Height (CM)', tracking=True)
    respiratory_rate = fields.Float('Respiratory Rate', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'general_clinic_visit_medical_history_rel', 'general_clinic_visit_id', 'medical_history_id', string='Medical History' ,compute= '_compute_medical_history')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'general_clinic_visit_allergic_history_rel', 'general_clinic_visit_id', 'allergic_history_id', string='Allergic History' ,compute= '_compute_allergic_history')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'rhs_anc_medication_history_rel', 'anc_id', 'medication_history_id', string='Medication History',compute= '_compute_medication_history')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'rhs_anc_surgical_history_rel', 'anc_id', 'surgical_history_id', string='Surgical History',compute= '_compute_surgical_history')
    current_complaint = fields.Char('Current Complaint', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    procedures_followed = fields.Char('Procedures Followed', tracking=True)
    procedure_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('non_emergency', 'Non-Emergency'),
        ('other', 'Other')
    ], string='Type Of Procedure', tracking=True)
    other_procedure_type = fields.Char('Other Type Of Procedure')
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?',tracking=True)
    referral_type=fields.Selection([
        ('incoming_referrals_from_phc', 'احالة واردة من مركز عناية صحية أولية'),
        ('incoming_referrals_from_hospital', 'احالة واردة من مشفى اخر'),
        ('incoming_referrals_from_mobile_clinic', 'احالة واردة من عيادة جوالة'),
        ('referral_for_delivery_to_sdp_paid', 'احالة صادرة للولادة في مركز مدفوع'),
        ('referral_for_delivery_to_sdp_notpaid', 'احالة صادرة للولادة في مركز مجاني'),
        ('referral_to_GBV_advanced_services', 'احالة صادرة لخدمات GBV'),
        ('referral_to_advanced_services', 'احالة صادرة الى خدمات متقدمة'),
        ('referral_to_turkey', 'احالة الى تركيا')
       
    ], string='To Which Center Were You Referred And What Was The Reason?')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'general_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'general_visit_id', string='Analysis Requests', tracking=True)
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'general_visit_id', string='Image Requests')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    notes = fields.Char('Notes', tracking=True)

    state_medication = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='medication Status Request', required=True, default='draft')
    state_analysis = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='analysis Status Request', required=True, default='draft')
    state_image = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='image Status Request', required=True, default='draft')

    @api.depends('company_id', 'clinic_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, self.clinic_id, fields.Date.today()).ids


    
    def confirm_record_medication(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.write({
            'state_medication': 'done'
        })
        
    def confirm_record_analysis(self):
        self.ensure_one()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.write({
            'state_analysis': 'done'
        })
    def confirm_record_image(self):
        self.ensure_one()
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state_image': 'done'
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