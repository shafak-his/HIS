from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHAwareness(models.Model):
    _name = 'em.hms.mh.awareness'
    _description = 'Mental Health Group Awareness Session'
    _rec_name = 'session_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_date = fields.Date('Session Date', required=True, tracking=True)
    facilitator_name = fields.Char('Activity Facilitator Name', tracking=True)
    activity_name = fields.Selection([
        ('depression', 'Depression'),
        ('loss_sadness', 'Loss And Sadness'),
        ('psychological_pressure', 'Psychological Pressure'),
        ('post_traumatic_stress_disorder', 'Post-traumatic Stress Disorder')
    ], string='Activity Name', tracking=True)
    boys_count = fields.Integer('#Males < 18', tracking=True)
    men_count = fields.Integer('#Males >= 18', tracking=True)
    girls_count = fields.Integer('#Females < 18', tracking=True)
    women_count = fields.Integer('#Females >= 18', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
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

    