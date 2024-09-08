from odoo import _, api, fields, models, exceptions, tools

class EmHmsNutritionDangerSignWoman(models.Model):
    _name = 'em.hms.nutrition.danger.sign.woman'
    _description = 'Danger Signs On Woman'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    

class EmHmsNutritionScreeningWoman(models.Model):
    _name = 'em.hms.nutrition.screening.woman'
    _description = 'Woman Screening for Acute Malnutrition'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    project_id = fields.Many2one('project.project', string='Project Number', tracking=True)
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Place Where The Service Is Provided', required=True, tracking=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    visit_type = fields.Selection([
        ('first', 'First'),
        ('follow_up', 'Follow-Up')
    ], string='Type Of Visit', required=True, tracking=True)
            
    muac_measurement = fields.Integer('MUAC Measurement', required=True, tracking=True)
    woman_status = fields.Selection([
        ('pregnant', 'pregnant'),
        ('breastfeeding', 'breastfeeding'),
        ('care_rovider', 'Care Provider'),
        ('first_trimester_pregnant', 'Pregnant In The First Trimester'),
        ('young_girl', 'Young Girl')
    ], string='Is The Beneficiary Pregnant, Breastfeeding, Or Otherwise?', required=True, tracking=True)
    infant_age = fields.Integer('Infant''s Age', tracking=True)
    nature_of_malnutrition = fields.Char(compute='_compute_nature_of_malnutrition', string='Nature Of Malnutrition')
    
    @api.depends('muac_measurement')
    def _compute_nature_of_malnutrition(self):
        for record in self:
            if record.muac_measurement:
                record.nature_of_malnutrition = 'MAM' if record.muac_measurement < 230 else 'NORMAL'
            else:
                record.nature_of_malnutrition = 'NOTHING'
    
    mother_program = fields.Selection([
        ('mam', 'MAM'),
        ('normal', 'NORMAL')
    ], string='What Is The Program The Mother Was Received With During The First Visit?', tracking=True)
    is_beneficiary_graduated = fields.Boolean('Has The Beneficiary Graduated?', tracking=True)
    graduation_outcome = fields.Selection([
        ('cured', 'Cured'),
        ('defaulter', 'Defaulter'),
        ('no_response', 'No Response'),
        ('move_to_another_program', 'Move To Another Program'),
        ('death', 'Death'),
        ('referrals', 'Referrals')
    ], string='What Are The Danger Signs?', tracking=True)
    is_death_or_deaulter = fields.Boolean(compute='_compute_is_death_or_deaulter', string='Is Death Or Deaulter')
    
    @api.depends('graduation_outcome')
    def _compute_is_death_or_deaulter(self):
        for record in self:
            record.is_death_or_deaulter = record.graduation_outcome == 'death' or record.graduation_outcome == 'defaulter'
              
    is_committed_to_examinations = fields.Boolean('Is The Mother Committed To Undergoing Periodic Examinations At The Center?', tracking=True)         
    is_violence_or_abuse_signs = fields.Boolean('Are There Any Visible Signs Of Any Violence Or Abuse?', tracking=True)
    is_danger_signs = fields.Boolean('Does The Beneficiary (Pregnant) Have Any Dnger Signs?', tracking=True)
    danger_signs_ids = fields.Many2many('em.hms.nutrition.danger.sign.woman', 'screening_danger_sign_woman_rel', 'screening_woman_id', 'danger_sign_woman_id', string='Danger Signs', tracking=True)
    
    is_beneficiary_referred = fields.Boolean('Based On The Beneficiary''s Condition, Has The Beneficiary Been Referred?', tracking=True)
    referral_place = fields.Char('Place Of Referral Beneficiary', default='شفق', tracking=True)
    is_supplements_distributed = fields.Boolean('Were Nutritional Supplements Distributed To The Beneficiary?')
    materials_distributed = fields.Selection([
        ('sup', 'Complementary Peanut Butter SUP (Envelope)'),
        ('lns_mq', 'Wawa Mum LNS-MQ Protective Butter (Envelope)'),
        ('nutri_butter', 'Nutri Butter (Envelope)'),
        ('mum', 'MUM Therapeutic Peanut Butter (Envelope)'),
        ('protective', 'Nutri Protective Peanut Butter (Envelope)'),
        ('biscuits', ' High-Energy Biscuits (Box)'),
        ('vitamins_minerals', 'Vitamins And Minerals Pills For Pregnant Women (One Pill)'),
        ('folic_iron', 'Folic Iron Pills (1 Pill)'),
        ('amoxicillin', 'Amoxicillin 250 mg Tab')
    ], string='The Type Of Materials Distributed', tracking=True)
    sup_qty = fields.Selection([
        ('15', '15'),
        ('30', '30')
    ], string='Supplementary Peanut Butter SUP (Sachet) Quantity', default='15', tracking=True)
    lns_mq_qty = fields.Integer('Wawa Mum LNS-MQ Protective Butter (Envelope) Quantity', default=30, tracking=True)
    nutri_butter_qty = fields.Integer('Quantity Of Nutri Butter (Envelope)', tracking=True)
    mum_qty = fields.Integer('MUM Therapeutic Peanut Butter Quantity (Envelope)', tracking=True)
    protective_qty = fields.Integer('Nutri Protective Peanut Butter (Sachet) Quantity', tracking=True)
    biscuits_qty = fields.Integer('Quantity Of High Energy Biscuits (Box)', default=14, tracking=True)
    vitamins_minerals_qty = fields.Integer('Quantity Of Vitamins And Minerals For Pregnant Woman (One Pill)', default=90, tracking=True)
    folic_iron_qty = fields.Integer('Quantity Of Folic Iron Pills', default=90, tracking=True)
    amoxicillin_qty = fields.Integer('Quantity Of Amoxicillin 250mg Tab', tracking=True)
    is_supplements_distributed2 = fields.Boolean('Was Another Item Distributed?', tracking=True)
    materials_distributed2 = fields.Selection([
        ('vitamins_minerals', 'Vitamins And Minerals Pills For Pregnant Women (One Pill)'),
        ('folic_iron', 'Folic Iron Pills (1 Pill)')
    ], string='The Type Of Materials Distributed', tracking=True)
    vitamins_minerals_qty2 = fields.Integer('Quantity Of Vitamins And Minerals For Pregnant Woman (One Pill)', tracking=True)
    folic_iron_qty2 = fields.Integer('Quantity Of Folic Iron Pills', tracking=True)
    
    is_breastfeedingf_session_offered = fields.Boolean('Is An BreastfeedingF Individual Counseling Session Offered?')
    main_session_topic = fields.Selection([
        ('breastfeeding', 'Breastfeeding'),
        ('relactating', 'Relactating'),
        ('beastfeeding_difficulties', 'Breastfeeding Difficulties'),
        ('pregnant_breastfeeding', 'Pregnant And Breastfeeding'),
        ('child_illness', 'Child Illness'),
        ('supplementary_feeding', 'Supplementary Feeding'),
        ('psychological_support', 'Psychological Support'),
        ('bms', 'BMS')
    ], string='Main Session Topic', tracking=True)
    
    session_topic_breastfeeding_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_breastfeeding_rel', 'screening_woman_id', 'session_topic_breastfeeding_id', string='Breastfeeding Topics', domain="[('category', '=', 'breastfeeding')]")
    other_breastfeeding_topic = fields.Char('Other Breastfeeding Topic', tracking=True)
    session_topic_relactating_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_relactating_rel', 'screening_woman_id', 'session_topic_relactating_id', string='Relactating Topics', domain="[('category', '=', 'relactating')]")
    other_relactating_topic = fields.Char('Other Relactating Topic', tracking=True)
    session_topic_breastfeeding_difficulties_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_breastfeeding_difficulties_rel', 'screening_woman_id', 'session_topic_breastfeeding_difficulties_id', string='Breastfeeding Difficulties Topics', domain="[('category', '=', 'breastfeeding_difficulties')]")
    other_breastfeeding_difficulties_topic = fields.Char('Other Breastfeeding Difficulties Topic', tracking=True)
    session_topic_pregnant_breastfeeding_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_pregnant_breastfeeding_rel', 'screening_woman_id', 'session_topic_pregnant_breastfeeding_id', string='Pregnant And Breastfeeding Topics', domain="[('category', '=', 'pregnant_breastfeeding')]")
    other_pregnant_breastfeeding_topic = fields.Char('Other Pregnant And Breastfeeding Topic', tracking=True)
    session_topic_child_illness_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_child_illness_rel', 'screening_woman_id', 'session_topic_child_illness_id', string='Child Illness Topics', domain="[('category', '=', 'child_illness')]")
    other_child_illness_topic = fields.Char('Other Child Illness Topic', tracking=True)
    session_topic_supplementary_feeding_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_supplementary_feeding_rel', 'screening_woman_id', 'session_topic_supplementary_feeding_id', string='Supplementary Feeding Topics', domain="[('category', '=', 'supplementary_feeding')]")
    other_supplementary_feeding_topic = fields.Char('Other Supplementary Feeding Topic', tracking=True)
    session_topic_psychological_support_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_psychological_support_rel', 'screening_woman_id', 'session_topic_psychological_support_id', string='Psychological Support Consultation Topics', domain="[('category', '=', 'psychological_support')]")
    other_psychological_support_topic = fields.Char('Other Psychological Support Consultation Topic', tracking=True)
    session_topic_bms_ids = fields.Many2many('em.hms.nutrition.topic', 'session_topic_bms_rel', 'screening_woman_id', 'session_topic_bms_id', string='BMS Topics', domain="[('category', '=', 'bms')]")
    other_bms_topic = fields.Char('Other BMS Topic', tracking=True)
    
    is_breastfeeding_topic = fields.Boolean(compute='_compute_is_breastfeeding_topic', string='Is Breastfeeding Topic')
    is_breastfeeding_topic_other = fields.Boolean(compute='_compute_is_breastfeeding_topic', string='Other Breastfeeding Topic')
    is_relactating_topic = fields.Boolean(compute='_compute_is_relactating_topic', string='Is Relactating Topic')
    is_relactating_topic_other = fields.Boolean(compute='_compute_is_relactating_topic', string='Other Relactating Topic')
    is_breastfeeding_difficulties_topic = fields.Boolean(compute='_compute_is_breastfeeding_difficulties_topic', string='Is Breastfeeding Difficulties Topic')
    is_breastfeeding_difficulties_topic_other = fields.Boolean(compute='_compute_is_breastfeeding_difficulties_topic', string='Other Breastfeeding Difficulties Topic')
    is_pregnant_breastfeeding_topic = fields.Boolean(compute='_compute_is_pregnant_breastfeeding_topic', string='Is Pregnant Breastfeeding Topic')
    is_pregnant_breastfeeding_topic_other = fields.Boolean(compute='_compute_is_pregnant_breastfeeding_topic', string='Other Pregnant Breastfeeding Topic')
    is_child_illness_topic = fields.Boolean(compute='_compute_is_child_illness_topic', string='Is Child Illness Topic')
    is_child_illness_topic_other = fields.Boolean(compute='_compute_is_child_illness_topic', string='Other Child Illness Topic')
    is_supplementary_feeding_topic = fields.Boolean(compute='_compute_is_supplementary_feeding_topic', string='Is Supplementary Feeding Topic')
    is_supplementary_feeding_topic_other = fields.Boolean(compute='_compute_is_supplementary_feeding_topic', string='Other Supplementary Feeding Topic')
    is_psychological_support_topic = fields.Boolean(compute='_compute_is_psychological_support_topic', string='Is Psychological Support Topic')
    is_psychological_support_topic_other = fields.Boolean(compute='_compute_is_psychological_support_topic', string='Other Psychological Support Topic')
    is_bms_topic = fields.Boolean(compute='_compute_is_bms_topic', string='Is BMS Topic')
    is_bms_topic_other = fields.Boolean(compute='_compute_is_bms_topic', string='Other BMS Topic')
    
    @api.depends('main_session_topic', 'session_topic_breastfeeding_ids')
    def _compute_is_breastfeeding_topic(self):
        for record in self:
            record.is_breastfeeding_topic = record.main_session_topic == 'breastfeeding'
            record.is_breastfeeding_topic_other = record.main_session_topic == 'breastfeeding' and 'Other' in record.session_topic_breastfeeding_ids.mapped('name') if record.session_topic_breastfeeding_ids else False
            
    @api.depends('main_session_topic', 'session_topic_relactating_ids')
    def _compute_is_relactating_topic(self):
        for record in self:
            record.is_relactating_topic = record.main_session_topic == 'relactating'
            record.is_relactating_topic_other = record.main_session_topic == 'relactating' and 'Other' in record.session_topic_relactating_ids.mapped('name') if record.session_topic_relactating_ids else False
            
    @api.depends('main_session_topic', 'session_topic_breastfeeding_difficulties_ids')
    def _compute_is_breastfeeding_difficulties_topic(self):
        for record in self:
            record.is_breastfeeding_difficulties_topic = record.main_session_topic == 'breastfeeding_difficulties'
            record.is_breastfeeding_difficulties_topic_other = record.main_session_topic == 'breastfeeding_difficulties' and 'Other' in record.session_topic_breastfeeding_difficulties_ids.mapped('name') if record.session_topic_breastfeeding_difficulties_ids else False
    
    @api.depends('main_session_topic', 'session_topic_pregnant_breastfeeding_ids')
    def _compute_is_pregnant_breastfeeding_topic(self):
        for record in self:
            record.is_pregnant_breastfeeding_topic = record.main_session_topic == 'pregnant_breastfeeding'
            record.is_pregnant_breastfeeding_topic_other = record.main_session_topic == 'pregnant_breastfeeding' and 'Other' in record.session_topic_pregnant_breastfeeding_ids.mapped('name') if record.session_topic_pregnant_breastfeeding_ids else False
            
    @api.depends('main_session_topic', 'session_topic_child_illness_ids')
    def _compute_is_child_illness_topic(self):
        for record in self:
            record.is_child_illness_topic = record.main_session_topic == 'child_illness'
            record.is_child_illness_topic_other = record.main_session_topic == 'child_illness' and 'Other' in record.session_topic_child_illness_ids.mapped('name') if record.session_topic_child_illness_ids else False
    
    @api.depends('main_session_topic', 'session_topic_supplementary_feeding_ids')
    def _compute_is_supplementary_feeding_topic(self):
        for record in self:
            record.is_supplementary_feeding_topic = record.main_session_topic == 'supplementary_feeding'
            record.is_supplementary_feeding_topic_other = record.main_session_topic == 'supplementary_feeding' and 'Other' in record.session_topic_supplementary_feeding_ids.mapped('name') if record.session_topic_supplementary_feeding_ids else False
            
    @api.depends('main_session_topic', 'session_topic_psychological_support_ids')
    def _compute_is_psychological_support_topic(self):
        for record in self:
            record.is_psychological_support_topic = record.main_session_topic == 'psychological_support'
            record.is_psychological_support_topic_other = record.main_session_topic == 'psychological_support' and 'Other' in record.session_topic_psychological_support_ids.mapped('name') if record.session_topic_psychological_support_ids else False
            
    @api.depends('main_session_topic', 'session_topic_bms_ids')
    def _compute_is_bms_topic(self):
        for record in self:
            record.is_bms_topic = record.main_session_topic == 'bms'
            record.is_bms_topic_other = record.main_session_topic == 'bms' and 'Other' in record.session_topic_bms_ids.mapped('name') if record.session_topic_bms_ids else False
            
    conduct_the_individual_session = fields.Selection([
        ('improvement', 'Improvement'),
        (' no_change', ' No Change'),
        ('retreat', 'Retreat'),
    ], string='Conduct The Individual Session', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_visit_date', 'CHECK (visit_date <= fields.Date.today())',
         'Visit Date Must Not Be Newer Than Today.'), ('check_muac_measurement', 'CHECK (muac_measurement >= 190 and muac_measurement <= 400)',
         'MUAC Measurement For Women should be between 190 and 400.'), ('check_infant_age', 'CHECK (infant_age >= 0 and infant_age <= 24)',
         'Infant Age should be between 0 and 24.')
    ]
    
    
    