from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPNC(models.Model):
    _name = 'em.hms.rhs.pnc'
    _description = 'RH Service - PNC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
    husband_name = fields.Char('Husband''s name', required=True)
    
    date_of_birth = fields.Date('Date Of Birth', required=True)
    type_of_birth = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Type of birth', required=True)
    is_baby_alive = fields.Boolean('Is the baby alive')
    body_weight = fields.Float('Body Weight', required=True, tracking=True)
    is_full_term_pregnancy = fields.Boolean('Full term pregnancy (<37 weeks)')
    place_of_birth = fields.Selection([
        ('home', 'Home'),
        ('medical_care_center', 'Medical Care Center'),
        ('hospital', 'Hospital')
    ], string='Place of birth', required=True, tracking=True)
    previous_complications = fields.Char('Previous pregnancy and birth complications')
    
    visit_ids = fields.One2many('em.hms.rhs.pnc.visit', 'pnc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    
    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count=len(record.visit_ids)
    