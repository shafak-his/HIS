from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPNC(models.Model):
    _name = 'em.hms.rhs.pnc'
    _description = 'PNC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    husband_name = fields.Char('Husband\'s Name', tracking=True)
    
    birth_date = fields.Date('Date Of Birth', tracking=True)
    birth_type = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Type Of Birth', tracking=True)
    is_baby_alive = fields.Boolean('Is The Baby Alive?', tracking=True)
    body_weight = fields.Float('Body Weight', tracking=True)
    is_full_term_pregnancy = fields.Boolean('Is Full Term Pregnancy (<37 weeks)?')
    birth_place = fields.Selection([
        ('home', 'Home'),
        ('medical_care_center', 'Medical Care Center'),
        ('hospital', 'Hospital')
    ], string='Place Of Birth', tracking=True)
    previous_complications = fields.Char('Previous Pregnancy And Birth Complications', tracking=True)
    
    visit_ids = fields.One2many('em.hms.rhs.pnc.visit', 'pnc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count=len(record.visit_ids)
            
    def action_get_pnc_visits_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'PNC Visits',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.pnc.visit',
            'domain': [('pnc_id', '=', self.id)],
            'context': "{'create': False}"
        }
    