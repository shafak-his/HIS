from odoo import _, api, fields, models, exceptions, tools


class EmHmsDialLithotripsy(models.Model):
    _name = 'em.hms.dial.lithotripsy'
    _description = 'Lithotripsy'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    weight = fields.Float('Weight', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    stone_location = fields.Selection([
        ('kidney', 'Kidney'),
        ('ureter', 'Ureter'),
        ('bladder', 'Bladder')
    ], string='Stone Location', tracking=True)

    session_type = fields.Selection([
        ('echo', 'ECHO'),
        ('ray', 'Ray')
    ], string='Session type', tracking=True)
    number_shots = fields.Integer('Number of Shots', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
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
    