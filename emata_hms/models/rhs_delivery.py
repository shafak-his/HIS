from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDelivery(models.Model):
    _name = 'em.hms.rhs.delivery'
    _description = 'Normal Delivery'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    admission_date = fields.Date('Date Of Admission', required=True, tracking=True)
    admitting_midwife_id = fields.Many2one('hr.employee', string='Name Of Admitting Midwife', required=True)
    doctor_id = fields.Many2one('hr.employee', string='Name Of Admitting Physician', required=True)
    husband_name = fields.Char('Name Of Husband', tracking=True)
    guardian_name = fields.Char('Name Of Patient\'s Guardian', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'delivery_medical_history_rel', 'delivery_id', 'medical_history_id', string='Medical History' ,compute= '_compute_medical_history')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'delivery_surgical_history_rel', 'delivery_id', 'surgical_history_id', string='Surgical History',compute= '_compute_surgical_history')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'delivery_medication_history_rel', 'delivery_id', 'medication_history_id', string='Medication History',compute= '_compute_medication_history')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'delivery_allergic_history_rel', 'delivery_id', 'allergic_history_id', string='Allergic History',compute= '_compute_allergic_history')
    initial_diagnosis = fields.Char('Initial Diagnosis', tracking=True, required=True)
    delivery_type= fields.Selection([
        ('normal_delivery', 'Normal Delivery'),
        ('c_section_elective', 'C-Section Elective'),
        ('c_section_emergency', 'C-Section Emergency'),
        ('assisted_vaginal_delivery', 'Assisted Vaginal Delivery'),
      
    ], string='Type Of Delivery', tracking=True,required=True)
    type_of_feeding = fields.Selection([
        ('breastfeeding', 'BreastFeeding'),
        ('artificial feeding', 'ArtificialFeeding'),
        ('combinationfeeding', 'CombinationFeeding')
        
      
        ], string='Type Of Feedings', tracking=True,required=True)
    reason_of_c_section=fields.Selection([
        ('t1', 'انبثاق أغشية باكر'),
        ('t2', 'انسمام حملي'),
        ('t3', 'انفصال مشيمة'),
        ('t4', 'تألم جنين (اضطراب اصغاء)'),
        ('t5', 'حمل عزيز'),
        ('t6', 'حمل مديد'),
        ('t7', 'خلع ورك خلقي عند الأم'),
        ('t8', 'عدم تناسب حوضي جنيني'),
        ('t9', 'عمليتين قصيريتين أو أكثر'),
        ('t10', 'فشل اتساع'),
        ('t11', 'فشل تقدم'),
         ('t12', 'مجيئ معيب عند المخاض'),
        ('t13', 'مشيمة مركزية'),
        ('t14', 'وجود انحلال في الدم أو نقص صفائح'),
        ('t15', 'وجود تمزق رحم حالي'),
         ('t16', 'وجود عدوى الإيدز أو فيروسية أخرى'),
        ('t17', 'وجود عمل جراحي سابق في الرحم'),
        ('other', 'اسباب اخرى')
    
    ], string='Reason Of C-Section', tracking=True, required=True)
    medical_signs_ids =fields.Many2many('em.hms.medical.sign', 'rhs_delivery_medicals_sign_rel', 'medical_signs_id', string='Medical Signs', tracking=True, required=True)#for delete
    medical_signs_id =fields.Many2one('em.hms.medical.sign', string='Medical Signs', tracking=True, required=True)
    
    number_of_newborn=fields.Integer('Number Of Newborn', tracking=True,required=True,default='1')
    child_name = fields.Char('Name Of Child', tracking=True)
    
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'delivery_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'delivery_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'delivery_visit_id', string='Image Requests')
    
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
    
    gestational_age = fields.Char('Gestational Age In Weeks', tracking=True,required=True)
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
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus'),
        ('inability_fluid_level1', 'Inability fluid level1'),
        ('inability_fluid_level2', 'Inability fluid level2'),
        ('inability_fluid_level3', 'Inability fluid level3'),
        ('severe_inability_fluid', 'severe inability fluid')
    ], string='Amniotic Fluid', tracking=True)
    
    birth_datetime = fields.Datetime('Date And Time Of Birth', tracking=True)
    birth_medication_ids = fields.Many2many('product.template', 'rhs_delivery_product_birth_medication_rel', 'delivery_id', 'product_id', string='Medications Used During Birth', domain="[('is_birth_medication', '=', True)]") #for delete
    birth_medications =fields.Text('Medications Used During Birth', tracking=True)
    birth_report = fields.Char('Birth Report', tracking=True)
    newborn_general_condition = fields.Selection([
        ('good_vitality', 'Good Vitality'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deceased', 'Deceased')
    ], string='General Condition Of The Child', tracking=True)
    newborn_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('two_males', 'Two Males'),
        ('two_females', 'Two Females'),
        ('one_male_and_one_female', 'One Male and one Female'),
        ('three_or_more', 'Three Newborn or more')
    ], string='Gender Of The Newborn', tracking=True,required=True)
    newborn_weight = fields.Float('Weight Of The Newborn', tracking=True)
    is_breastfeeding_first_hour = fields.Boolean('Breastfeeding Within The First Hour', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
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
    discharge_datetime = fields.Datetime('Date Of Discharge And Time', tracking=True)
    discharge_supervising_physician_id = fields.Many2one('hr.employee', string='Supervising Physician')
    discharge_duty_midwife_id = fields.Many2one('hr.employee', string='Midwife On Duty')
    patient_condition = fields.Selection([
        ('to_home', 'To Home'),
        ('another_hospital', 'Another Hospital'),
        ('deathCaseMother', 'Death Case Mother'),
        ('other', 'Other')
    ], string='Patient''s Condition', tracking=True )
    newborn_condition = fields.Selection([
        ('to_home', 'To Home'),
        ('another_hospital', 'Another Hospital'),
        ('transfer_to_care', 'Transfer To Care'),
        ('transfer_to_incubators', 'Transfer To Incubators'),
        ('deathCaseNewborn', 'Death Case Newborn'),
        ('deaths_inside_facility', 'Neonatal Deaths inside the Health Facility'),
    ], string='Newborn''s Condition', tracking=True)
    deathCase_report_number=fields.Char('Death Case Report number', tracking=True)
    patient_companion_name = fields.Char('Patient''s Companion''s Name', tracking=True)
    patient_companion_relationship = fields.Char('Relationship', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    labor_ids = fields.One2many('em.hms.labor', 'delivery_id', string='Labor Monitoring')
    labors_count = fields.Integer(compute='_compute_labors_count', string='Labors Count')
    vital_sign_ids = fields.One2many('em.hms.vital.sign', 'delivery_id', string='Vital Signs Monitoring')
    vital_signs_count = fields.Integer(compute='_compute_vital_signs_count', string='Vital Signs Reports')
    post_birth_ids = fields.One2many('em.hms.post.surgery', 'delivery_id', string='Post-Birth Monitoring')
    post_births_count = fields.Integer(compute='_compute_post_births_count', string='Post-Birth Reports')
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
    