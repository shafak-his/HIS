from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANC(models.Model):
    _name = 'em.hms.rhs.anc'
    _description = 'RH Service - ANC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
    number_of_previous_cesarean_sections = fields.Integer('Number of previous cesarean sections', required=True)
    family_medical_history = fields.Char('Family medical history')
    is_breastfeeding = fields.Boolean('Breastfeeding', required=True)
    drug_history = fields.Char('Drug history')
    is_smoking = fields.Boolean('Smoking')
    medical_history = fields.Char('Medical History')
    allergic_history = fields.Char('Allergic History')
    is_referral = fields.Boolean('Has there been a referral?', required=True, tracking=True)
    referral_center_reason = fields.Char('To which center were you referred and what was the reason for referral?')
    complications = fields.Char('Previous pregnancy and birth complications')
    
    number_of_pregnancies = fields.Integer('Number Of Pregnancies', required=True)
    number_of_premature_births = fields.Integer('Number of premature births', required=True)
    number_of_miscarriages = fields.Integer('Number of miscarriages', required=True)
    live_births = fields.Integer('Live Births', required=True)
    number_of_deaths = fields.Integer('Number of deaths', required=True)
    last_menstrual_date = fields.Date('First day of last menstrual period', required=True)
    expected_due_date = fields.Date('Expected due date', required=True)
    nature_of_previous_births = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Nature of previous births', required=True)
    
    visit_ids = fields.One2many('em.hms.rhs.anc.visit', 'anc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    
    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count=len(record.visit_ids)
    