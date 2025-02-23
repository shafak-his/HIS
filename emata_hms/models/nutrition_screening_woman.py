from odoo import _, api, fields, models, exceptions, tools

class EmHmsNutritionDangerSignWoman(models.Model):
    _name = 'em.hms.nutrition.danger.sign.woman'
    _description = 'Danger Signs On Woman'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)

class EmHmsNutritionScreeningWoman(models.Model):
    _name = 'em.hms.nutrition.screening.woman'
    _description = 'Woman Screening for Acute Malnutrition'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
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
    is_pbw = fields.Boolean(compute='_compute_is_pbw', string='Compute Is Pregnant OR Breastfeeding Woman')
    infant_age = fields.Integer('Infant''s Age', tracking=True)
    malnutrition_nature = fields.Char(compute='_compute_malnutrition_nature', string='Nature Of Malnutrition')
    
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
    is_death_or_defaulter = fields.Boolean(compute='_compute_is_death_or_defaulter', string='Is Death Or Defaulter')
              
    is_committed_to_examinations = fields.Boolean('Mother Committed To Undergoing Periodic Examinations At The Center?', tracking=True)         
    is_violence_or_abuse_signs = fields.Boolean('Any Visible Signs Of Any Violence Or Abuse?', tracking=True)
    is_danger_signs = fields.Boolean('Does The Beneficiary (Pregnant) Have Any Dnger Signs?', tracking=True)
    danger_signs_ids = fields.Many2many('em.hms.nutrition.danger.sign.woman', 'screening_danger_sign_woman_rel', 'screening_woman_id', 'danger_sign_woman_id', string='Danger Signs', tracking=True)
    
    is_beneficiary_referred = fields.Boolean('Has The Beneficiary Been Referred?', tracking=True)
    referral_place = fields.Char('Referral Place', default='Shafak', tracking=True)
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
    
    visit_number = fields.Selection([
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('fourth', 'Fourth'),
        ('fifth', 'Fifth'),
        ('sixth', 'Sixth'),
        ('seventh', 'Seventh'),
        ('eighth', 'Eighth'),
        ('ninth', 'Ninth')
    ], string='Specify The Visit Number', tracking=True)
    is_iycf_session_offered = fields.Boolean('Is An BreastfeedingF IYCF Individual Counseling Session Offered?')
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
    
    topic_ids = fields.One2many('em.hms.nutrition.screening.woman.topic', 'session_id', string='Topics')

    conduct_individual_session = fields.Selection([
        ('improvement', 'Improvement'),
        (' no_change', ' No Change'),
        ('retreat', 'Retreat'),
    ], string='Conduct The Individual Session', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    _sql_constraints = [
        ('check_visit_date', 'CHECK (visit_date <= CURRENT_DATE)', 'Visit date cannot be in future.'),
        ('check_muac_measurement', 'CHECK (muac_measurement >= 190 and muac_measurement <= 400)', 'MUAC Measurement For Women should be between 190 and 400.'),
        ('check_infant_age', 'CHECK (infant_age >= 0 and infant_age <= 24)', 'Infant Age should be between 0 and 24.')
    ]

    @api.depends('woman_status')
    def _compute_is_pbw(self):
        for record in self:
            record.is_pbw = record.woman_status == 'pregnant' or record.woman_status == 'breastfeeding'
            
    @api.depends('graduation_outcome')
    def _compute_is_death_or_defaulter(self):
        for record in self:
            record.is_death_or_defaulter = record.graduation_outcome == 'death' or record.graduation_outcome == 'defaulter'
    
    @api.depends('muac_measurement')
    def _compute_malnutrition_nature(self):
        for record in self:
            if record.muac_measurement:
                record.malnutrition_nature = 'MAM' if record.muac_measurement < 230 else 'NORMAL'
            else:
                record.malnutrition_nature = 'NOTHING'
    
class EmHmsNutritionGroupSessionTopic(models.Model):
    _name = 'em.hms.nutrition.screening.woman.topic'
    _description = 'Woman Screening for Acute Malnutrition Topic'
    
    session_id = fields.Many2one('em.hms.nutrition.screening.woman', string='Session', ondelete='cascade')
    topic_id = fields.Many2one('em.hms.nutrition.topic', string='Main Topic', required=True)
    sub_topic_ids = fields.Many2many('em.hms.nutrition.topic', 'em_nutrition_screening_women_topic_rel', 'topic_id', 'sub_topic_id', string='Sub-Topic', required=True)
    other_sub_topics = fields.Char('Other Sub-Topics')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)    
    