from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSInfertilityTreatment(models.Model):
    _name = 'em.hms.rhs.infertility.treatment'
    _description = 'Infertility Treatment'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    visit_date = fields.Datetime('Date Of Visit', required=True, tracking=True)
    husband_name = fields.Char('Husband\'s Name', tracking=True)
    miarriages_count = fields.Integer('# Marriages', tracking=True)
    pregnancies_count = fields.Integer('# Pregnancies', tracking=True)
    miscarriages_count = fields.Integer('# Miscarriages', tracking=True)
    deaths_count = fields.Integer('# Deaths', tracking=True)
    last_marriage_date = fields.Date('Last Marriage Date', tracking=True)
    births = fields.Integer('# Births', tracking=True)
    alives_count = fields.Integer('# Alives', tracking=True)
    normal_births_count = fields.Integer('# Normal Bitrhs', tracking=True)
    cesarean_births_count = fields.Integer('# Cesarean Bitrhs', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'infertility_treatment_medical_history_rel', 'infertility_treatment_id', 'medical_history_id', string='Medical History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'infertility_treatment_surgical_history_rel', 'infertility_treatment_id', 'surgical_history_id', string='Surgical History')
    
    is_husband_tested = fields.Boolean('Has The Husband Been Tested?', tracking=True)
    husband_analysis = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ], string='Husband''s Analysis', tracking=True)
    explain_abnormal = fields.Char('If Abnormal, Explain', tracking=True)
    husband_analysis_date = fields.Date('Last Marriage Date', tracking=True)
    wife_hormonal_tests = fields.Char('Hormonal Tests Performed On The Wife', tracking=True)
    is_ovulation_natural1 = fields.Boolean('Monitoring Natural Ovulation (1st Month)', tracking=True)
    ovum_measuring_natural1 = fields.Integer('Measuring The Ovum (1st Month)', tracking=True)
    is_ovulation_natural2 = fields.Boolean('Monitoring Natural Ovulation (2nd Month)', tracking=True)
    ovum_measuring_natural2 = fields.Integer('Measuring The Ovum (2nd Month)', tracking=True)
    is_ovulation_natural3 = fields.Boolean('Monitoring Natural Ovulation (3rd Month)', tracking=True)
    ovum_measuring_natural3 = fields.Integer('Measuring The Ovum (3rd Month)', tracking=True)
    medication_request_ids = fields.One2many('em.hms.medication.request', 'infertility_treatment_id', string='Stimulation Medications')
    is_ovulation_treatment1 = fields.Boolean('Monitoring Ovulation After Treatment (1st Month)', tracking=True)
    ovum_measuring_treatment1 = fields.Integer('Measuring The Ovum (1st Month)', tracking=True)
    is_ovulation_treatment2 = fields.Boolean('Monitoring Ovulation After Treatment (2nd Month)', tracking=True)
    ovum_measuring_treatment2 = fields.Integer('Measuring The Ovum (2nd Month)', tracking=True)
    is_ovulation_treatment3 = fields.Boolean('Monitoring Ovulation After Treatment (3rd Month)', tracking=True)
    ovum_measuring_treatment3 = fields.Integer('Measuring The Ovum (3rd Month)', tracking=True)
    
    uterus_image = fields.Binary('Shadow Image Of The Uterus And Appendages', tracking=True)
    is_intrauterine_injected = fields.Boolean('Intrauterine Injected?', tracking=True)
    is_laparoscopy = fields.Boolean('Laparoscopy?', tracking=True)
    laparoscopy_result = fields.Char('Laparoscopy Result', tracking=True)
    laparoscopy_attachment = fields.Binary('Laparoscopy Attachment', tracking=True)
    is_hysteroscopy = fields.Boolean('Hysteroscopy?', tracking=True)
    hysteroscopy_result = fields.Char('Hysteroscopy Result', tracking=True)
    hysteroscopy_attachment = fields.Binary('Hysteroscopy Attachment', tracking=True)
    analysis_request_ids = fields.One2many('em.hms.analysis.request', 'infertility_treatment_id', string='Request An X-Ray')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_visit_date', 'CHECK (visit_date <= CURRENT_DATE)', 'Visit Date Must Not Be in Future.'),
        ('check_last_marriage_date', 'CHECK (last_marriage_date <= CURRENT_DATE)', 'Last Marriage Date Must Not Be Newer Than Today.'),
    ]
    
    def confirm_record(self):
        self.ensure_one()
        self.medication_request_ids.generate_sale_order()
        self.write({
            'state': 'done'
        }) 