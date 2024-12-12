from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSEDCClinicalCondition(models.Model):
    _name = 'em.hms.rhs.edc.clinical.condition'
    _description = 'Clinical Condition'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsRHSEDCSymptom(models.Model):
    _name = 'em.hms.rhs.edc.symptom'
    _description = 'Symptoms'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsRHSEDCSign(models.Model):
    _name = 'em.hms.rhs.edc.sign'
    _description = 'Signs'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsRHSEDCASCUS(models.Model):
    _name = 'em.hms.rhs.edc.ascus'
    _description = 'ASCUS'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)

class EmHmsRHSEDCPlan(models.Model):
    _name = 'em.hms.rhs.edc.plan'
    _description = 'Management And Follow-Up Plan'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsRHEDC(models.Model):
    _name = 'em.hms.rhs.edc'
    _description = 'EDC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
        
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    session_date = fields.Date('Session Date', required=True, tracking=True)
    marital_status = fields.Selection([
        ('active_sexually', 'Active Sexually'),
        ('inactive_sexually', 'Inactive Sexually (Divorced, Widow, Traveling Husband)')
    ], string='Marital Status', tracking=True)
    number_marriages = fields.Integer('# Marriages', tracking=True)
    first_marriage_age = fields.Integer('Age At First Marriage (In Years)', tracking=True)
    first_pregnancy_age = fields.Integer('Age At First Pregnancy (In Years)', tracking=True)
    number_pregnancies = fields.Integer('# Pregnancies', tracking=True)
    number_births = fields.Integer('# Births', tracking=True)
    is_disabled = fields.Boolean('Is Disabled?', tracking=True)
    
    clinical_condition_ids = fields.Many2many('em.hms.rhs.edc.clinical.condition', 'edc_clinical_condition_rel', 'edc_id', 'edc_clinical_condition_id', string='Clinical Conditions', tracking=True)
    is_contraceptives = fields.Boolean(compute='_compute_is_contraceptives_hormonic_drugs', string='Is Contraceptives Duration') #To Fahd
    is_hormonic_drugs = fields.Boolean(compute='_compute_is_contraceptives_hormonic_drugs', string='Is Hormonic Drugs') #To Fahd
    
    @api.depends('clinical_condition_ids')
    def _compute_is_contraceptives_hormonic_drugs(self):
        for record in self:
            record.is_contraceptives = 'Contraceptives' in record.clinical_condition_ids.mapped('name')
            record.is_hormonic_drugs = 'Hormonic Drugs' in record.clinical_condition_ids.mapped('name')
            
    contraceptives_duration = fields.Char('Duration Of Use Of Hormonal Contraceptives', tracking=True)
    hormonal_medications = fields.Char('Other Hormones (Duration And Type Of Use)', tracking=True)
    last_menstrual_date = fields.Date('Last Menstrual Date', tracking=True)
    smear_day = fields.Integer('Day Of Smear Test In Relation To Menstrual Period', tracking=True)
    is_smear_taken = fields.Boolean('Have a Smear Test Been Before?', tracking=True)
    last_smear_date = fields.Date('Date Of Last Smear', tracking=True)
    last_smear_result = fields.Char('Last Smear Result', tracking=True)
    symptom_ids = fields.Many2many('em.hms.rhs.edc.symptom', 'edc_symptom_rel', 'edc_id', 'edc_symptom_id', string='Symptoms', tracking=True)
    is_other_symptom = fields.Boolean(compute='_compute_is_other_symptom', string='Is Other Symptom')
    
    @api.depends('symptom_ids')
    def _compute_is_other_symptom(self):
        for record in self:
            record.is_other_symptom = 'Other' in record.symptom_ids.mapped('name')
    other_symptom = fields.Char('Other Symptom', tracking=True)
    sign_ids = fields.Many2many('em.hms.rhs.edc.sign', 'edc_sign_rel', 'edc_id', 'edc_sign_id', string='Signs: Neck Appearance', tracking=True)
    is_other_sign = fields.Boolean(compute='_compute_is_other_sign', string='Is Other Symptom')
    
    @api.depends('sign_ids')
    def _compute_is_other_sign(self):
        for record in self:
            record.is_other_sign = 'Other' in record.sign_ids.mapped('name')
    other_sign = fields.Char('Other Sign', tracking=True)
    ascus_ids = fields.Many2many('em.hms.rhs.edc.ascus', 'edc_ascus_rel', 'edc_id', 'edc_ascus_id', string='Atypical Squamous Cells Of Undetermined Significance', tracking=True)
    is_microscopic_evaluation_accepted = fields.Boolean('Is Microscopic Evaluation Accepted?', tracking=True)
    eval_rejection_reason = fields.Char('Reason of Rejecting Evaluation', tracking=True)
    smear_microscopic_evaluation = fields.Selection([
        ('normal', 'Normal'),
        ('acute_inflammatory', 'Acute Inflammatory'),
        ('chronic_inflammatory', 'Chronic Inflammatory'),
        ('abnormal', 'Abnormal'),
        ('borderline_result', 'Borderline Result'),
        ('cancerous', 'Cancerous')
    ], string='Smear Microscopic Evaluation', tracking=True)
    is_asch = fields.Boolean('ASCH?', tracking=True)
    is_nos = fields.Boolean('NOS?', tracking=True)
    limit_result = fields.Selection([
        ('lsli', '(CIN I) LSLI'),
        ('hsli', '(CIN III - CIN II) HSLI')
    ], string='Limit Result', tracking=True)
    cancer_result = fields.Selection([
        ('cis', 'CIS'),
        ('squamous_cell_carcinoma', 'Squamous Cell Carcinoma'),
        ('adenocarcinoma', 'Adenocarcinoma')
    ], string='Cancer Result', tracking=True)
    plan_ids = fields.Many2many('em.hms.rhs.edc.plan', 'edc_plan_rel', 'edc_id', 'edc_plan_id', string='Management And Follow-Up Plans', tracking=True)
    is_resmearing_plan = fields.Boolean(compute='_compute_is_resmearing_plan', string='Is Resmearing Plan') #To Fahd
    
    @api.depends('plan_ids')
    def _compute_is_resmearing_plan(self):
        for record in self:
            record.is_resmearing_plan = 'Resmearing' in record.plan_ids.mapped('name')
            
    number_months_resmear = fields.Integer('Resmear After (Month(s))', tracking=True)
    
    supervisor_id = fields.Many2one('hr.employee', 'Supervisor Doctor', tracking=True)
    examiner_name = fields.Char('Sample Examiner Name', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    _sql_constraints = [
        ('check_session_date', 'CHECK (session_date <= CURRENT_DATE)', 'Session Date Must Not Be Newer Than Today.'),
        ('check_last_menstrual_date', 'CHECK (last_menstrual_date <= CURRENT_DATE)', 'Last Menstrual Date Must Not Be Newer Than Today.'),
        ('check_last_smear_date', 'CHECK (last_smear_date <= CURRENT_DATE)', 'Last Smear Date Must Not Be Newer Than Today.'),
    ]