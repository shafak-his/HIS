from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANC(models.Model):
    _name = 'em.hms.rhs.anc'
    _description = 'ANC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    cesarean_sections_count = fields.Integer('# Previous Cesarean Sections', tracking=True)
    family_medical_history = fields.Char('Family Medical History', tracking=True)
    is_breastfeeding = fields.Boolean('Is Breastfeeding?', tracking=True)
    is_smoking = fields.Boolean('Is Smoking?', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
    previous_complications = fields.Char('Previous Pregnancy And Birth Complications', tracking=True)
    
    pregnancies_count = fields.Integer('# Pregnancies', tracking=True)
    premature_births_count = fields.Integer('Number of Premature Births', tracking=True)
    miscarriages_count = fields.Integer('# Miscarriages', tracking=True)
    live_births = fields.Integer('Live Births', tracking=True)
    deaths_count = fields.Integer('# Deaths', tracking=True)
    last_menstrual_date = fields.Date('First Day Of Last Menstrual Period', tracking=True)
    expected_due_date = fields.Date('Expected Due Date', tracking=True)
    nature_of_previous_births = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Nature Of Previous Births', tracking=True)
    
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'rhs_anc_medical_history_rel', 'anc_id', 'medical_history_id', string='Medical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'rhs_anc_medication_history_rel', 'anc_id', 'medication_history_id', string='Medication History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'rhs_anc_allergic_history_rel', 'anc_id', 'allergic_history_id', string='Allergic History')
    
    visit_ids = fields.One2many('em.hms.rhs.anc.visit', 'anc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    allowed_project_ids = fields.Many2many('project.project', compute='_compute_allowed_project_ids', string='Allowed Projects', compute_sudo=True)

    @api.onchange('allowed_project_ids')
    def _onchange_allowed_project_ids(self):
        if self.allowed_project_ids:
            self.project_id = self.allowed_project_ids[0].id

    @api.depends('company_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, False, fields.Date.today()).ids

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
    