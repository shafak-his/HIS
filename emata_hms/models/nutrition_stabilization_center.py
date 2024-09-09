from odoo import _, api, fields, models, exceptions, tools
from dateutil.relativedelta import relativedelta


class EmHmsNutritionStabilizationCenter(models.Model):
    _name = 'em.hms.nutrition.stabilization.center'
    _description = 'Stabilization Center'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    project_id = fields.Many2one('project.project', string='Project Number', tracking=True)
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Place Where The Service Is Provided', required=True, tracking=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    is_child_accepted = fields.Boolean('Has It Been Accepted?', tracking=True)
    age_in_months = fields.Integer(compute='_compute_age_in_months', string='Child''s Age In Months')
    
    @api.depends('patient_id', 'visit_date')
    def _compute_age_in_months(self):
        for record in self:
            if record.patient_id.birth_date and record.visit_date:
                difference = relativedelta(record.visit_date, record.patient_id.birth_date)
                record.age_in_months = difference.months + 12 * difference.years
            else:
                record.age_in_months = 0
            
    is_zscore_lt_minus3 = fields.Boolean('Is Zscore Less Than (-3)?', tracking=True)
    muac_measurement = fields.Integer('MUAC Measurement', required=True, tracking=True)
    is_bilateral_edema = fields.Boolean('Is there Bilateral Edema In The Child?', required=True, tracking=True)
    zscore_measurement = fields.Selection([
        ('normal', 'Normal Under 6 Months'),
        ('lt_minus_3', 'Less Than (-3)'),
        ('minus_3_to_minus_2', 'From (-3) To Less Than (-2)'),
        ('gt_eq_minus_2', '(-2) And Above')
    ], string='Zscore Measurement For Children', tracking=True)
    
    is_danger_signs = fields.Boolean('Are There Danger Signs For Children?', tracking=True)
    danger_signs_ids = fields.Many2many('em.hms.nutrition.danger.sign.child', 'stabilization_center_danger_sign_rel', 'stabilization_center_id', 'danger_sign_child_id', string='Danger Signs', tracking=True)
    nature_of_malnutrition = fields.Char(compute='_compute_nature_of_malnutrition', string='Nature Of Malnutrition')
    
    @api.depends('is_bilateral_edema', 'is_zscore_lt_minus3', 'age_in_months', 'zscore_measurement', 'is_danger_signs')
    def _compute_nature_of_malnutrition(self):
        for record in self:
            record.nature_of_malnutrition = ''
            if record.age_in_months < 6:
                if record.is_bilateral_edema or record.is_zscore_lt_minus3:
                    record.nature_of_malnutrition = 'SAM With Complications'
            else:
                if record.zscore_measurement == 'lt_minus_3' or record.is_danger_signs:
                    record.nature_of_malnutrition = 'SAM With Complications'
                if not record.is_danger_signs and record.zscore_measurement != 'lt_minus_3':
                    record.nature_of_malnutrition = 'SAM'

    medicines_type = fields.Char('What Type Of Medicines?', tracking=True)
    is_confusion_gone = fields.Boolean('Is The Confusion Gone?', tracking=True)
    is_pain_gone = fields.Boolean('Is The Pain Gone?', required=True, tracking=True)
    is_child_accepted_transitional = fields.Boolean('Child >= 6 Months Accepted Into The Second (Transitional) Stage?', tracking=True)
    is_child_accepted_rehabilitation = fields.Boolean('Child >= 6 Months Accepted Accepted Into The Second (Rehabilitation) Stage?', tracking=True)
    is_appetite_test_passed = fields.Boolean('Did The Appetite Test Pass?', tracking=True)
    
    is_beneficiary_graduated = fields.Boolean('Has The Beneficiary Graduated?', tracking=True)
    graduation_outcome = fields.Selection([
        ('no_response', 'No Response'),
        ('move_to_otp_program', 'Move To OTP Program')
    ], string='What Are The Danger Signs?', tracking=True)
    is_supplements_distributed = fields.Boolean('Were Nutritional Supplements Distributed To The Beneficiary?', required=True, tracking=True)
    materials_distributed = fields.Selection([
        ('f100_milk', 'F100 milk'),
        ('f75_milk', 'F75 milk')
    ], string='The Type Of Materials Distributed', tracking=True)
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
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_visit_date', 'CHECK (visit_date <= CURRENT_DATE)',
         'Visit Date Must Not Be Newer Than Today.'), ('check_muac_measurement', 'CHECK (muac_measurement >= 70 and muac_measurement <= 200)',
         'MUAC Measurement For Children should be between 70 and 200.')
    ]
    
    
    show_question_accepted_transitional = fields.Boolean(compute='_compute_show_question_accepted_transitional', string='Show Question Accepted Transitional')
    
    @api.depends('age_in_months', 'is_confusion_gone', 'is_pain_gone')
    def _compute_show_question_accepted_transitional(self):
        for record in self:
            record.show_question_accepted_transitional = record.age_in_months >= 6 and record.is_confusion_gone and record.is_pain_gone
            
    show_question_is_graduated = fields.Boolean(compute='_compute_show_question_is_graduated', string='Show Question Is Graduated')
    
    @api.depends('is_appetite_test_passed', 'is_pain_gone', 'is_zscore_lt_minus3')
    def _compute_show_question_is_graduated(self):
        for record in self:
            record.show_question_is_graduated = record.is_appetite_test_passed and record.is_pain_gone and record.is_zscore_lt_minus3
    