from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANC(models.Model):
    _name = 'em.hms.rhs.anc'
    _description = 'RH Service - ANC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True)
    cesarean_sections_count = fields.Integer('Number Of Previous Cesarean Sections', required=True, tracking=True)
    family_medical_history = fields.Char('Family Medical History', tracking=True)
    is_breastfeeding = fields.Boolean('Is Breastfeeding?', required=True, tracking=True)
    drug_history = fields.Char('Drug History', tracking=True)
    is_smoking = fields.Boolean('Is Smoking?', tracking=True)
    medical_history = fields.Char('Medical History', tracking=True)
    allergic_history = fields.Char('Allergic History', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', required=True, tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason For Referral?', tracking=True)
    previous_complications = fields.Char('Previous Pregnancy And Birth Complications', tracking=True)
    
    pregnancies_count = fields.Integer('Number Of Pregnancies', required=True, tracking=True)
    premature_births_count = fields.Integer('Number of Premature Births', required=True, tracking=True)
    miscarriages_count = fields.Integer('Number Of Miscarriages', required=True, tracking=True)
    live_births = fields.Integer('Live Births', required=True, tracking=True)
    deaths_count = fields.Integer('Number Of Deaths', required=True, tracking=True)
    last_menstrual_date = fields.Date('First Day Of Last Menstrual Period', required=True, tracking=True)
    expected_due_date = fields.Date('Expected Due Date', required=True, tracking=True)
    nature_of_previous_births = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Nature Of Previous Births', required=True, tracking=True)
    
    visit_ids = fields.One2many('em.hms.rhs.anc.visit', 'anc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count = len(record.visit_ids)
            
            
    def action_get_anc_visits_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Periodic Visits',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.anc.visit',
            'domain': [('anc_id', '=', self.id)],
            'context': "{'create': False}"
        }
    