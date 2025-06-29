from odoo import _, api, fields, models, exceptions, tools



class EmHmsRHSANC(models.Model):
    _name = 'em.hms.rhs.anc'
    _description = 'ANC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    cesarean_sections_count = fields.Integer('# Previous Cesarean Sections', tracking=True)
    family_medical_history = fields.Char('Family Medical History', tracking=True)
    is_breastfeeding = fields.Boolean('Is Breastfeeding?', tracking=True)
    type_of_feeding = fields.Selection([
        ('breastfeeding', 'BreastFeeding'),
        ('artificial feeding', 'ArtificialFeeding'),
        ('combinationfeeding', 'CombinationFeeding')
        
      
        ], string='Type Of Feedings', tracking=True)
    is_smoking = fields.Boolean('Is Smoking?', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
    previous_complications = fields.Char('Previous Pregnancy And Birth Complications', tracking=True)
    last_menstrual_date = fields.Date('First Day Of Last Menstrual Period', tracking=True)
    expected_due_date = fields.Date('Expected Due Date', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'rhs_anc_medical_history_rel', 'anc_id', 'medical_history_id', string='Medical History')
    medication_history_ids = fields.Many2many('em.hms.medication.history', 'rhs_anc_medication_history_rel', 'anc_id', 'medication_history_id', string='Medication History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'rhs_anc_allergic_history_rel', 'anc_id', 'allergic_history_id', string='Allergic History')
    surgical_history_ids = fields.Many2many('em.hms.surgical.history', 'rhs_anc_surgical_history_rel', 'anc_id', 'surgical_history_id', string='Surgical History')
    previous_obstetric_history_ids = fields.One2many('em.hms.rhs.anc.previous.obstetric','previous_obstetrich_history_id', string='Previous Obstetric History')
    visit_ids = fields.One2many('em.hms.rhs.anc.visit', 'anc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    type_of_previous_births = fields.Selection([
        ('liveborn', 'Liveborn'),
        ('premature', 'Premature'),
        ('miscarriage', 'Miscarriage'),
        ('stillborn', 'Stillborn')
      
        ], string='Type Of Previous Births', tracking=True)
    nature_of_previous_births = fields.Selection([
        ('liveborn', 'Liveborn'),
        ('premature', 'Premature'),
        ('miscarriage', 'Miscarriage'),
        ('stillborn', 'Stillborn')
      
        ], string='Type Of Previous Births', tracking=True)
    pregnancies_count = fields.Selection([
        ('liveborn', 'Liveborn'),
        ('premature', 'Premature'),
        ('miscarriage', 'Miscarriage'),
        ('stillborn', 'Stillborn')
      
        ], string='Type Of Previous Births', tracking=True)
    live_births = fields.Selection([
        ('liveborn', 'Liveborn'),
        ('premature', 'Premature'),
        ('miscarriage', 'Miscarriage'),
        ('stillborn', 'Stillborn')
      
        ], string='Type Of Previous Births', tracking=True)



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
    