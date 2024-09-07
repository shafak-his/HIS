from odoo import _, api, fields, models, exceptions, tools
from dateutil.relativedelta import relativedelta

class EmHmsNutritionDangerSignChild(models.Model):
    _name = 'em.hms.nutrition.danger.sign.child'
    _description = 'Danger Signs On Child'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    

class EmHmsNutritionScreeningChild(models.Model):
    _name = 'em.hms.nutrition.screening.child'
    _description = 'Child Screening for Acute Malnutrition'
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
    age_in_months = fields.Integer(compute='_compute_age_in_months', string='Child''s Age In Months')
    
    @api.depends('patient_id', 'visit_date')
    def _compute_age_in_months(self):
        for record in self:
            if record.patient_id.birth_date and record.visit_date:
                difference = relativedelta(record.visit_date, record.patient_id.birth_date)
                record.age_in_months = difference.months + 12 * difference.years
            else:
                record.age_in_months = 0
            
    muac_measurement = fields.Integer('MUAC Measurement', required=True, tracking=True)
    zscore_measurement = fields.Selection([
        ('normal', 'Normal Under 6 Months'),
        ('lt_minus_3', 'Less Than (-3)'),
        ('minus_3_to_minus_2', 'From (-3) To Less Than (-2)'),
        ('gt_eq_minus_2', '(-2) And Above')
    ], string='Zscore Measurement For Children', tracking=True)
    nature_of_malnutrition = fields.Char(compute='_compute_nature_of_malnutrition', string='Nature Of Malnutrition')
    
    @api.depends('muac_measurement', 'zscore_measurement')
    def _compute_nature_of_malnutrition(self):
        for record in self:
            if record.zscore_measurement == 'lt_minus_3':
                record.nature_of_malnutrition = 'SAM'
            if record.zscore_measurement == 'minus_3_to_minus_2':
                record.nature_of_malnutrition = 'MAM'
            if record.muac_measurement < 115:
                record.nature_of_malnutrition = 'SAM'
            elif record.muac_measurement < 125:
                record.nature_of_malnutrition = 'MAM'
            else:
                record.nature_of_malnutrition = 'NORMAL'
                
    is_bilateral_edema = fields.Boolean('Is there Bilateral Edema In The Child?', tracking=True)
    is_danger_signs = fields.Boolean('Are There Danger Signs For Children?', tracking=True)
    danger_signs_ids = fields.Many2many('em.hms.nutrition.danger.sign.child', 'screening_danger_sign_child_rel', 'screening_child_id', 'danger_sign_child_id', string='Danger Signs', tracking=True)
    child_condition_at_first_visit = fields.Selection([
        ('sam', 'SAM'),
        ('mam', 'MAM'),
        ('sam_complications', 'SAM With Complications'),
        ('normal', 'Normal')
    ], string='Child Condition At First Visit', tracking=True)
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
    
    is_sam_case = fields.Boolean(compute='_compute_is_sam_case', string='Is SAM Case')
    
    @api.depends('muac_measurement', 'zscore_measurement', 'is_bilateral_edema')
    def _compute_is_sam_case(self):
        for record in self:
            record.is_sam_case = record.muac_measurement < 115 or record.zscore_measurement == 'lt_minus_3' or record.is_bilateral_edema == True
    
    @api.onchange('is_bilateral_edema', 'is_danger_signs', 'muac_measurement')
    def _get_default_nature_of_sam(self):
        if self.is_bilateral_edema == True:
            self.nature_of_sam = 'sam'
        else:
            if self.muac_measurement < 115 and self.is_danger_signs:
                self.nature_of_sam = 'sam_complications'
            
    nature_of_sam = fields.Selection([
        ('sam', 'SAM'),
        ('sam_complications', 'SAM With Complications')
    ], string='Nature Of SAM', tracking=True)
    is_violence_or_abuse_signs = fields.Boolean('Are There Any Visible Signs Of Any Violence Or Abuse?', tracking=True)
    
    @api.onchange('visit_type', 'is_bilateral_edema', 'is_danger_signs', 'nature_of_malnutrition')
    def _get_default_is_beneficiary_referred(self):
            self.is_beneficiary_referred = self.visit_type == 'first' and (self.is_bilateral_edema == True or self.is_danger_signs == True or self.nature_of_malnutrition == 'SAM' or self.nature_of_malnutrition == 'MAM')
            
    is_beneficiary_referred = fields.Boolean('Based On The Beneficiary''s Condition, Has The Beneficiary Been Referred?', tracking=True)
    referral_place = fields.Char('Place Of Referral Beneficiary', default='شفق', tracking=True)
    is_supplements_distributed = fields.Boolean('Were Nutritional Supplements Distributed To The Beneficiary?')
    materials_distributed = fields.Selection([
        ('nut', 'NUT Therapeutic Peanut Butter (Sachet)'),
        ('sup', 'Complementary Peanut Butter SUP (Envelope)'),
        ('lns_mq', 'Wawa Mum LNS-MQ Protective Butter (Envelope)'),
        ('nutri_butter', 'Nutri Butter (Envelope)'),
        ('mum', 'MUM Therapeutic Peanut Butter (Envelope)'),
        ('protective', 'Nutri Protective Peanut Butter (Envelope)'),
        ('biscuits', ' High-Energy Biscuits (Box)'),
        ('vitamins_minerals', 'Vitamins And Minerals For Children (Envelope)'),
        ('bp5', 'BP-5'),
        ('f100_milk', 'F100 milk'),
        ('f75_milk', 'F75 milk')
    ], string='The Type Of Materials Distributed', tracking=True)
    nut_qty = fields.Integer('NUT Therapeutic Peanut Butter Quantity (Envelope)', tracking=True)
    sup_qty = fields.Selection([
        ('15', '15'),
        ('30', '30')
    ], string='Supplementary Peanut Butter SUP (Sachet) Quantity', default='15', tracking=True)
    lns_mq_qty = fields.Integer('Wawa Mum LNS-MQ Protective Butter (Envelope) Quantity', default=30, tracking=True)
    nutri_butter_qty = fields.Integer('Quantity Of Nutri Butter (Envelope)', tracking=True)
    mum_qty = fields.Integer('MUM Therapeutic Peanut Butter Quantity (Envelope)', tracking=True)
    protective_qty = fields.Integer('Nutri Protective Peanut Butter (Sachet) Quantity', tracking=True)
    biscuits_qty = fields.Integer('Quantity Of High Energy Biscuits (Box)', default=14, tracking=True)
    vitamins_minerals_qty = fields.Integer('Quantity Of Vitamins And Minerals For Children (Envelope)', default=30, tracking=True)
    bp5_qty = fields.Integer('Quantity Of Bp-5 (Tablet)', default=2, tracking=True)
    f100_milk_qty = fields.Integer('F100 Milk', tracking=True)
    f75_milk_qty = fields.Integer('F75 Milk', tracking=True)
    
    first_visit_number = fields.Selection([
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
    is_simple_assessment = fields.Boolean('Simple And Quick Assessment For Mothers Of Children Under 2 Years Old', default=True, tracking=True)
    is_simple_to_comprehensive_assessment = fields.Boolean('Has It Been Converted Into A Comprehensive Evaluation? ', tracking=True)
    reason_for_comprehensive = fields.Char('Reason For Transferring To A Comprehensive Program', tracking=True)
    problem_suffering = fields.Selection([
        ('non_exclusive_breastfeeding', 'Non-Exclusive Breastfeeding'),
        ('complementary_foods', 'Problems With Complementary Foods')
    ], string='The Problem The Child Is Suffering From', tracking=True)
    
    @api.onchange('problem_suffering')
    def _get_advice_provided(self):
        if self.problem_suffering == 'non_exclusive_breastfeeding':
            self.advice_provided = 'exclusive_breastfeeding'
        elif self.problem_suffering == 'complementary_foods':
            self.advice_provided = 'supplementary_food'
        else:
            return ''
    advice_provided = fields.Selection([
        ('exclusive_breastfeeding', 'An Exclusive Breastfeeding Session'),
        ('supplementary_food', 'Supplementary Food Session')
    ], string='Advice Provided', tracking=True)
    is_exclusive_breastfeeding = fields.Boolean(' Is There Exclusive Breastfeeding BF?', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_visit_date', 'CHECK (visit_date <= fields.Date.today())',
         'Visit Date Must Not Be Newer Than Today.'), ('check_muac_measurement', 'CHECK (muac_measurement >= 70 and muac_measurement <= 200)',
         'MUAC Measurement For Children should be between 70 and 200.')
    ]
    
    